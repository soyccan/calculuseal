import requests
import json
import urllib.parse
import time
import logging
import os
import os.path
from random import randint

def solve(equation, img_dir):
    '''solve equation and get answer in images
    str equation: in wolframalpha format
    str img_dir: directory in which to place result images
    int @returns: random id of which directory is for images storage, or -1 upon failure
    '''
    logging.debug(f'equation: {equation}')

    inp = urllib.parse.quote(equation)
    timestamp = str(int(time.time())) + '000'
    r = requests.get(f'https://www.wolframalpha.com/input/api/v1/code?ts={timestamp}')
    proxycode = r.json().get('code')

    logging.debug(f'timestamp={timestamp}')
    logging.debug(f'inp={inp}')
    logging.debug(f'proxycode={proxycode}')
    logging.debug('response: ' + r.text)

    r = requests.get(
        f'https://www.wolframalpha.com/input/json.jsp?assumptionsversion=2&async=true&banners=raw&debuggingdata=false&format=image,plaintext,imagemap,sound,minput,moutput&formattimeout=8'
        f'&input={inp}&output=JSON&parsetimeout=5&podinfosasync=true&proxycode={proxycode}&recalcscheme=parallel&sbsdetails=true&scantimeout=0.5&sponsorcategories=true&statemethod=deploybutton&storesubpodexprs=true',
        headers={
            'Host': 'www.wolframalpha.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Referer': f'https://www.wolframalpha.com/input/?i={inp}'})

    logging.debug('response: ' + r.text)
    j = r.json()
    # logging.debug(json.dumps(j, indent=4, sort_keys=True))

    Id = -1
    while True:
        Id = randint(1, 100000000)
        try:
            os.mkdir(f'{img_dir}/{Id}')
        except FileExistsError:
            pass
        else:
            break

    queryresult = j.get('queryresult')
    logging.debug(f'queryresult={queryresult}')
    if not queryresult or queryresult.get('error') == None or queryresult.get('error') == True:
        return -1
    pods = queryresult.get('pods')
    for pod in pods:
        title = pod.get('title')
        subpods = pod.get('subpods')
        for subpod in subpods:
            # TODO: file types other than JPEG
            path = os.path.join(img_dir, Id, title+'.jpg')
            logging.debug(f'writing to {path}')
            img = subpod.get('img').get('src')
            open(path, 'wb').write(requests.get(img).content)

    return Id


'''
curl -i -s -k  -X $'GET' \
    -H $'Host: www.wolframalpha.com' \
    -H $'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0' \
    -H $'Referer: https://www.wolframalpha.com/input/?i=x%3D+sinh+y%3D(e%5E(y)+-e%5E(-y)+)+%2F(2)' \
    $'https://www.wolframalpha.com/input/json.jsp?assumptionsversion=2&async=true&banners=raw&debuggingdata=false&format=image,plaintext,imagemap,sound,minput,moutput&formattimeout=8&input=x%3D+sinh+y%3D(e%5E(y)+-e%5E(-y)+)+%2F(2)&output=JSON&parsetimeout=5&podinfosasync=true&proxycode=013f63f9b1558278657a406d9ebaa254&recalcscheme=parallel&sbsdetails=true&scantimeout=0.5&sponsorcategories=true&statemethod=deploybutton&storesubpodexprs=true'

    -H $'Connection: close' \
    -H $'Accept: application/json, text/plain, */*' \
    -H $'Accept-Language: zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3' \
    -H $'Accept-Encoding: gzip, deflate' \
    -H $'Cookie: WR_SID=140.113.139.77.1546393465923402; wa_tr_session=78344558257384540000; JSESSIONID=85CBE0331170C9982B4BA07FED2B90C0; __cookie_consent=2' \
    -b $'WR_SID=140.113.139.77.1546393465923402; wa_tr_session=78344558257384540000; JSESSIONID=85CBE0331170C9982B4BA07FED2B90C0; __cookie_consent=2' \

{
    "queryresult": {
        "datatypes": "",
        "encryptedEvaluatedExpression": "NmFwWjCu+QNanR5Xc4dj7DzqPoqhuo3niJytgXHZ7bdEvgY31Gn2LfyK/b9dBfLD",
        "encryptedParsedExpression": "JdngEbAoBiZUEg2JFFbvtK1hugrE7B71YZ3Y6g+gpoblMdvEw/RuQbdZmYEZ5YUI",
        "error": false,
        "host": "https://www4b.wolframalpha.com",
        "id": "MSPa51821a755ah26b7a3f0000001a9dc66b20gi9056",
        "numpods": 3,
        "parsetimedout": false,
        "parsetiming": 0.659,
        "pods": [
            {
                "error": false,
                "id": "Input",
                "numsubpods": 1,
                "position": 100,
                "scanner": "Identity",
                "subpods": [
                    {
                        "expressionID": "MSP51841a755ah26b7a3f00000026fgdd027g3i48d7",
                        "img": {
                            "alt": "x = sinh(y) = 1/2 (e^y - e^(-y))",
                            "height": 36,
                            "src": "https://www4b.wolframalpha.com/Calculate/MSP/MSP51851a755ah26b7a3f0000003h74hf5c07319693?MSPStoreType=image/gif&s=50",
                            "themes": "1,2,3,4,5,6,7,8,9,10,11,12",
                            "title": "x = sinh(y) = 1/2 (e^y - e^(-y))",
                            "type": "Default",
                            "width": 161
                        },
                        "infos": {
                            "img": {
                                "alt": "sinh(x) is the hyperbolic sine function",
                                "height": "12",
                                "src": "https://www4b.wolframalpha.com/Calculate/MSP/MSP51861a755ah26b7a3f00000031eaa3f9e9ai1hgi?MSPStoreType=image/gif&s=50",
                                "title": "sinh(x) is the hyperbolic sine function",
                                "width": "208"
                            },
                            "links": [
                                {
                                    "text": "Documentation",
                                    "title": "Mathematica",
                                    "url": "http://reference.wolfram.com/language/ref/Sinh.html"
                                },
                                {
                                    "text": "Properties",
                                    "title": "Wolfram Functions Site",
                                    "url": "http://functions.wolfram.com/ElementaryFunctions/Sinh"
                                },
                                {
                                    "text": "Definition",
                                    "title": "MathWorld",
                                    "url": "http://mathworld.wolfram.com/HyperbolicSine.html"
                                }
                            ],
                            "text": "sinh(x) is the hyperbolic sine function"
                        },
                        "minput": "x == Sinh[y] == (E^y - E^(-y))/2",
                        "plaintext": "x = sinh(y) = 1/2 (e^y - e^(-y))",
                        "subpodformats": [
                            {
                                "name": "Mathematical",
                                "type": "TeX [formulas],TeXFragment [formulas],MathML [formulas]"
                            },
                            {
                                "name": "RasterImage",
                                "type": "GIF [entire output],GIF [formulas],JPEG [entire output],JPEG [formulas],PNG [entire output],PNG [formulas],TIFF [entire output],TIFF [formulas],JPEG2000 [entire output],JPEG2000 [formulas],BMP [entire output],BMP [formulas],PXR [entire output],PXR [formulas],SCT [entire output],SCT [formulas]"
                            },
                            {
                                "name": "VectorGraphics",
                                "type": "PDF [entire output],PDF [formulas],EPS [entire output],EPS [formulas],SVG [entire output],SVG [formulas]"
                            },
                            {
                                "name": "Web",
                                "type": "GIF [entire output],GIF [formulas],PNG [entire output],PNG [formulas],JPEG [entire output],JPEG [formulas],SVG [entire output],SVG [formulas],MathML [formulas]"
                            },
                            {
                                "name": "Wolfram Language",
                                "type": "CDF [entire output],CDF [computable data],CDF [formatted results],NB,Package [computable data],Package [formatted results],Package [formulas]"
                            }
                        ],
                        "title": ""
                    }
                ],
                "title": "Input"
            },
            {
                "deploybuttonstates": [
                    {
                        "input": "MSP51921a755ah26b7a3f00000038cc305cd6cfha3a",
                        "name": "Approximate form",
                        "storedOnRedis": true
                    },
                    {
                        "input": "MSP51931a755ah26b7a3f00000014hiadb4h2e2h68h",
                        "name": "Step-by-step solution",
                        "stepbystep": true,
                        "storedOnRedis": true,
                        "style": "stepbystepsolution"
                    }
                ],
                "error": false,
                "id": "SymbolicSolution",
                "numsubpods": 1,
                "position": 200,
                "primary": true,
                "scanner": "Reduce",
                "subpods": [
                    {
                        "expressionID": "MSP51881a755ah26b7a3f00000031accd4cb5980ffc",
                        "imagemap": {
                            "rect": {
                                "assumptions": "\"ClashPrefs\" -> {\"Math\"}",
                                "bottom": 20,
                                "left": 27,
                                "query": "i+n+%CF%80",
                                "right": 52,
                                "title": "i n \u03c0",
                                "top": 2
                            }
                        },
                        "img": {
                            "alt": "y = i \u03c0 n, n element Z",
                            "height": 22,
                            "src": "https://www4b.wolframalpha.com/Calculate/MSP/MSP51891a755ah26b7a3f0000000ga66154c7a644ih?MSPStoreType=image/gif&s=50",
                            "themes": "1,2,3,4,5,6,7,8,9,10,11,12",
                            "title": "y = i \u03c0 n, n element Z",
                            "type": "Default",
                            "width": 550
                        },
                        "infos": {
                            "img": {
                                "alt": "Z is the set of integers",
                                "height": "12",
                                "src": "https://www4b.wolframalpha.com/Calculate/MSP/MSP51901a755ah26b7a3f000000513647f5025aaa56?MSPStoreType=image/gif&s=50",
                                "title": "Z is the set of integers",
                                "width": "127"
                            },
                            "links": [
                                {
                                    "text": "Documentation",
                                    "title": "Documentation",
                                    "url": "http://reference.wolfram.com/language/ref/Integers.html"
                                },
                                {
                                    "text": "Definition",
                                    "title": "MathWorld",
                                    "url": "http://mathworld.wolfram.com/Z.html"
                                }
                            ],
                            "text": "Z is the set of integers"
                        },
                        "minput": "Reduce[Sinh[y] == 0, y]",
                        "moutput": "{{y == I Pi C[1], Element[C[1], Integers]}}",
                        "plaintext": "y = i \u03c0 n, n element Z",
                        "subpodformats": [
                            {
                                "name": "Mathematical",
                                "type": "TeX [formulas],TeXFragment [formulas],MathML [formulas]"
                            },
                            {
                                "name": "RasterImage",
                                "type": "GIF [entire output],GIF [formulas],JPEG [entire output],JPEG [formulas],PNG [entire output],PNG [formulas],TIFF [entire output],TIFF [formulas],JPEG2000 [entire output],JPEG2000 [formulas],BMP [entire output],BMP [formulas],PXR [entire output],PXR [formulas],SCT [entire output],SCT [formulas]"
                            },
                            {
                                "name": "VectorGraphics",
                                "type": "PDF [entire output],PDF [formulas],EPS [entire output],EPS [formulas],SVG [entire output],SVG [formulas]"
                            },
                            {
                                "name": "Web",
                                "type": "GIF [entire output],GIF [formulas],PNG [entire output],PNG [formulas],JPEG [entire output],JPEG [formulas],SVG [entire output],SVG [formulas],MathML [formulas]"
                            },
                            {
                                "name": "Wolfram Language",
                                "type": "CDF [entire output],CDF [computable data],CDF [formatted results],NB,Package [computable data],Package [formatted results],Package [formulas]"
                            }
                        ],
                        "title": ""
                    }
                ],
                "title": "Roots"
            },
            {
                "deploybuttonstates": [
                    {
                        "input": "MSP51961a755ah26b7a3f0000003c6fgc4ih34114i2",
                        "name": "Step-by-step solution",
                        "stepbystep": true,
                        "storedOnRedis": true,
                        "style": "stepbystepsolution"
                    }
                ],
                "error": false,
                "id": "IntegerSolution",
                "numsubpods": 1,
                "position": 300,
                "primary": true,
                "scanner": "Reduce",
                "subpods": [
                    {
                        "expressionID": "MSP51941a755ah26b7a3f0000001f3f3i61c8325d6i",
                        "img": {
                            "alt": "y = 0",
                            "height": 22,
                            "src": "https://www4b.wolframalpha.com/Calculate/MSP/MSP51951a755ah26b7a3f000000185e69hg4c68b5d9?MSPStoreType=image/gif&s=50",
                            "themes": "1,2,3,4,5,6,7,8,9,10,11,12",
                            "title": "y = 0",
                            "type": "Default",
                            "width": 550
                        },
                        "minput": "Reduce[Sinh[y] == 0, y, Integers]",
                        "moutput": "{{y == 0}}",
                        "plaintext": "y = 0",
                        "subpodformats": [
                            {
                                "name": "Mathematical",
                                "type": "TeX [formulas],TeXFragment [formulas],MathML [formulas]"
                            },
                            {
                                "name": "RasterImage",
                                "type": "GIF [entire output],GIF [formulas],JPEG [entire output],JPEG [formulas],PNG [entire output],PNG [formulas],TIFF [entire output],TIFF [formulas],JPEG2000 [entire output],JPEG2000 [formulas],BMP [entire output],BMP [formulas],PXR [entire output],PXR [formulas],SCT [entire output],SCT [formulas]"
                            },
                            {
                                "name": "VectorGraphics",
                                "type": "PDF [entire output],PDF [formulas],EPS [entire output],EPS [formulas],SVG [entire output],SVG [formulas]"
                            },
                            {
                                "name": "Web",
                                "type": "GIF [entire output],GIF [formulas],PNG [entire output],PNG [formulas],JPEG [entire output],JPEG [formulas],SVG [entire output],SVG [formulas],MathML [formulas]"
                            },
                            {
                                "name": "Wolfram Language",
                                "type": "CDF [entire output],CDF [computable data],CDF [formatted results],NB,Package [computable data],Package [formatted results],Package [formulas]"
                            }
                        ],
                        "title": ""
                    }
                ],
                "title": "Integer root"
            }
        ],
        "recalculate": "https://www4b.wolframalpha.com/api/v2/recalc.jsp?id=MSPa51811a755ah26b7a3f0000006aac81c28ee34g7b8724354141067481742&output=JSON",
        "related": "https://www4b.wolframalpha.com/api/v2/relatedQueries.jsp?id=MSPa51831a755ah26b7a3f00000033d409aigiahfe0i8724354141067481742",
        "server": "50",
        "sponsorCategories": {
            "CampaignID": 254,
            "ExternalLinkQ": false,
            "Frequency": 1.0,
            "HoverImage": "",
            "HoverText": "",
            "HoverURL": "",
            "HoverURLText": "",
            "MainHoverImage": "",
            "MainImage": "examples-pages-chemistry.png",
            "MainText": "",
            "MainURL": "http://www.wolframalpha.com/examples/Chemistry.html",
            "MainURLText": "",
            "Score": 1,
            "SponsorID": 9
        },
        "success": true,
        "timedout": "",
        "timedoutpods": "",
        "timing": 1.416,
        "version": "2.6"
    }
}


'''
