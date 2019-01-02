import sys
import base64
import requests
import json
import logging

def translate(file_path):
    """translate the image specified by file_path into equations of WolframAlpha format
    str file_path: full path of image file
    str @returns: equations of WolframAlpha format
    """
    b64str = base64.b64encode(open(file_path, "rb").read()).decode()
    r = requests.post(
        "https://api.mathpix.com/v3/latex",
        data=json.dumps({
            "metadata": {
                "count": 17,
                "mode": "solver",
                "user_id":"16E45C4A-46F7-4F94-A95F-EDBF8F463941"
            },
            "url": "data:image/jpeg;base64," + b64str,
            "formats": {
                "latex_confidence_rate_threshold":0.5,
                "latex_confidence_threshold":0,
                "wolfram":"true"
            }}),
            # 'src': image_uri,
            # 'formats': ['latex_normal', 'latex_styled']}),
        headers={
            # "app_id": "trial",
            # "app_key": "34f1a4cea0eaca8540c95908b4dc84ab",
            "app_id": "mathpix_ios",
            "app_key": "025c3298dae222b4e6b4cc7758814e5e",
            'User-Agent': 'Mathpix/4.4.2.2 CFNetwork/894 Darwin/17.4.0',
            'Host': 'api.mathpix.com',
            "Content-type": "application/json"})
    j = r.json()
    logging.debug('response:')
    logging.debug(json.dumps(j, indent=4, sort_keys=True))
    return j.get('wolfram')

'''
curl -i -s -k  -X $'POST' \
    -H $'Host: api.mathpix.com' \
    -H $'Content-Type: application/json' \
    -H $'app_id: mathpix_ios' \
    -H $'app_key: 025c3298dae222b4e6b4cc7758814e5e' \
    -H $'User-Agent: Mathpix/4.4.2.2 CFNetwork/894 Darwin/17.4.0' \
    --data-binary $'{\"metadata\":{\"count\":17,\"mode\":\"solver\",\"user_id\":\"16E45C4A-46F7-4F94-A95F-EDBF8F463941\"},\"url\":\"data:image\\/jpeg;base64,\\/9j\\/4AAQSkZJRgABAQAASABIAAD\\/4QBMRXhpZgAATU0AKgAAAAgAAgESAAMAAAABAAEAAIdpAAQAAAABAAAAJgAAAAAAAqACAAQAAAABAAADsqADAAQAAAABAAAB2gAAAAD\\/7QA4UGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAAAA4QklNBCUAAAAAABDUHYzZjwCyBOmACZjs+EJ+\\/8AAEQgB2gOyAwEiAAIRAQMRAf\\/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC\\/\\/EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29\\/j5+v\\/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC\\/\\/EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29\\/j5+v\\/bAEMACQkJCQkJEAkJEBYQEBAWHhYWFhYeJh4eHh4eJi4mJiYmJiYuLi4uLi4uLjc3Nzc3N0BAQEBASEhISEhISEhISP\\/bAEMBCwwMEhESHxERH0szKjNLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS\\/\\/dAAQAPP\\/aAAwDAQACEQMRAD8A9SoFBoGag0FNFJS0AJRRRQAnWlpKU0CEpPpS0maBi9KTvQR6UUwYGiikoAWlxSUmaQhfekOaBR1oASikp2KACm0402mAdaKWkoADTRS0vagQ2l7UGkoAKBRRQA0ikZFdcOMinYzS0DGqqqNq9KcaSloEFJS0UAFFIaBmgBcUnWg0UgCkpaDTAaaUU3HenChgL2paSigYGjmikNAhDTaXmkNAAOlO7UmKMGgApMUpFIBQBHIdqlvSuIba8pJ6k5xXY3hIt3x12muTtofMlAI6UAjr7JAlsgHGRmrYApiKFQAdhT6QxMU0ipO1JTAjNMxUhppHFAiMrUZHNT44qMigRA1Rkc1ZxUbDnIoArnFQsABVojPNRMmeaYivjPWmkVPt7U1gcYoFYrkUwip9vGKjI5oERUU8g0mKBDDimmn02gBwo96SjNADuOtHWk7UUALjNKKQZxSigBM0vGeaSg0AHXmlpo604kUCF7UUhwaX2oAKSiigYmDRinU3mgQlOHQ0YpCPSgYCkpcUnU0gAH0oJ5xR0NLj1piE604UnendKQCU2nEcU0jNMB1ApnengcZNAB14pMUvI6UYpANopelJjNA0Ge1HPSjBBzSDJoELjHWgUmKXFACUlL0pOtMBuKYRUgHrSHpikMrkZphqZhULcUhjMUYp3PvRg+9Az\\/\\/Q9OJyeKkqIdakOQKg0DPNO5xxTc0tAB0pBS9aSgQtFFJQMTFFJS0xC80lFAoATFFL2xSUhi0n1pRRQISijtSc96BiilPFNHWlJzQITg0mKBSmgQhopKUdKYxO9GaOaTFIQtFGcUDpTADSUGigA6UUADNB60DFxTadnim0CCloooATk0ZweaWmmgBSabmg0tADqTFLmkoATilo4o60DCm+9OpDxQIO1FIKCTQAhOKQdaU0cUAFHHeg5pCKAFxmlPFCjjmjigCneY+ztmsHTkP2sDrjJNbt8cQHFUtKjPzSMOtAzcHTNA60e1JQId1pKKSgYUh5p3Tmm0CGYxSYzUmKbigRDg0xgetT4ppoArkUwgd6nIzTNvagCAr6UwjNWSKjKnqaAKpSmFcdKtEd6Zt9aYrFUjvTCKskYHFMIHSgkrkUmKlIxxTSMUCIzSU4jmkoAKKWjgUAJmlpKWgBKXrRR1oAU00U7jGKPpQIb0pwpDTsigEJ3o4p3XmmnimMXPrSfSijpSAMmijNFAhM+tB9qT3pfekMQdc0760lJQAuaXPrSDnNLjPSgkCc8UUYoxTGJ0pcetLikJoAdwRSHGKBSHmgBB1p2Mc0gNFIAooFBPemAHFM5NOPPFIBgUgEzzR3paTPNAAQaYakJJFR4pghhXJprLzUp9RSGkMq5ej56n2ijaKQ9T\\/\\/0fTh1px5puadUGgtA5pvbFOFAhaSk70UDFooooASkpc0GgQUlFKOKYCUtJnNHekMdmkNLSGgQmcUcU2loAXikPHSlNJmgBKUkUUlABSA0UdKYBnmiikBoAXFFHtRQISkpc0qjuaACk60GgGgAopKWgYUUUHpQIQUYpKWgANFJS96QADSZozRTAKXFGaBQAUh5paQigAFITzSikFACY5pelBGDmigBMk0tJRzQAtFHWigCneLuj2juafaweTHjoT1qwVDdadmgA7UtJS5pAITRSHrS0wAmkoNJ7UALSUtISKAAVGRzmpKbQBHTSKl70zFAiPGKQ9KlK8U2gCHFRleanxSEUAVcUwr3qyRzUZFArFcL61GyelWSB1ppHFArFYrmmYNWWWoiMZHemBFQafikINBIzmgGnY9aaPegBOvNFKRSUAHWlxSUGgQdaUUlKOM0ALmkJ7UlOoGFNwc5p1JQAuKPrRQRmgQlLnijFHWgoQ9KQinmkWkIVfSgj0p2c0lMkTmjmiigYUlKPejNACCl9qM5ooATGKOc0tIaAEHJpaF4pT7UAMPWnDpSGn44pANNNp5GajIPagYp4pp9adjNHtTEgwDUZFP7YpD0pAR4oxTqKAP\\/9L07GTTqaDjpS54rM0FHWlpucUo5pgLRRikoAKO9FJTAWk60ZopAFFGaBTASlFLRQIKSjvRSASlFFJTADRSA0UgCiil4oASiikpiENFL1pKBi9aO1GKKBCdaUUnvS0AJRRS0DDimn2oPSkFAg6U7PrQaTvQAh5pe1GKDQAUopop2KQDeTRnNBoFMQUvajNFAxOBS5zSGkoAXtSUGm5oAfSdaKSgAoJxxSZpcE8mgAozS9KQGgQuaKTNFAxe9O4xSAUhOKAFoNFIaACigUtACZoAHWiigApvSnUlADTSU4000AHWkwO9OxSUCGdaZipselNxg5oAhK1GVJqwR60wjvQgK5GOKYQRU5HFNI\\/OgRWYEUwj1FWCuaaR3pgVyBTMHFTleKjIOKCSLAppFS49aaRmgCOm1Jim4oBjKXqKOlAoELQTRnjFHWkA3I70uaQjJpcUwHd6M4pKMZoELS4pKPakMWgZxSUtMBMinY4poxTulAhM0UYNFMQtIaWjvSGJSU6kPWkA0Zp1HQUUxB25pMUuKB1pDHYAppxmnUlMBuOaXJo6GlNACUzPNPppxmkwFpD0oHNOIpgiOmj5uakIpdo60AR4oxUlFID\\/0\\/Twvc0pppY4pCc1BoLkUoNIBS470AOJFNopRQAmAaMAcUtJz1oASjNLQKBBS0DmigEFJQaMGgAxRRzmjFABSUtA5oAbilAooFMYGilNNoAQUUtJxQIKKUUe1AB2pMUvJ60UCGmig0daAEFLmikoAPrS4xTadmgANJSHrS0AGaOaXFN70AKKXNJSUABpTTaM5NAC0CiigAJpopxpPegBevWm8ZpaaeaAA9aMUuaQmgBKUGjNA5NADsA0dKXHemmgAxRRRQAtJxmlNNoAf9KSkpRQAd6WkoHWgANLSd6KAFpDRmigBDTeKd3zSEc0AJS4oA5p1ADaTFKBQaAIyKQipMU0igCHFMI5qfHakIoEQFaZtqwRTMUAQMtRlaskc0wrQKxWK5qMjFWSBTCKYiuR6U3FTlB1qPA7UCIcCkIA6VNtppWgCLFKOKdikNIBtHelNFMQlKKTkc0o5oYCUlL0NJjmgB\\/amr15o7YpQMUCHYpTxxSD3pTQISilxSH2pjClFJRSAM0daKCccUANPPFL0oHPNHFAC0gpe1HWhAFJgZ5pcUmKAFNJS0ZoASk604ijtSABxRQTQKYBiilpaAG4NGDTqKAP\\/9T0smkHWg81IoqDQWl7UhooAUUdKWjGaBDc0ZoxRzmmMBS0UmaQBnsKCD0oopiEp2eKQ80cYpAGeKOtFLmmAlJntSnmigBKMYoNHagBc02lpKACko6UtAgxxxSHinZFJigYnNLRSUCA0g4NLSUABpKKUcUAJiilpv0oAWgc80UUMBaTrSE4oGO9IBeabzT8+lNpgNzS0hz2p1ACYpaM0p4oAaaTFL1pRQA3IpMUN1oBoAWkNKDzTScmgAFOpMjNKemKAAGlzSdBRQAtJTscUlADecUCnAUhNABn0p1NAoNABS0mKUcUAB60UlKOlAgAooo6mgYGkNKaSgBBTvakApcUAGKQ0uaTrQAHim49aXNJQAcGm4p9IKAImBpAPWpCOaQ9aBERFMPFTkUwigCvimkVNikKmgRXK0wqcc1Yx60wigCDFRsO9WCMUwgmmIh28ZpmDmrBBFMK4pAQY5pSCTTyKKYiMikHFPakoEMpR60uKbzmgB2AetKT6UlH0oELnNKPWm57UA0AOJ5pOQaKSgBxBFJRkkZNGKADnpQaM0c0AGMUYpc0UAJR1pTgCjNACUYNFFACUUtHWmAUGkpaQxCDSj3pKdQAuO9Ge1KBmjvQIMUYowKMCmB\\/\\/9X0gZJ4qwBgVCnWp6hmg09aXtSdaXNMBaSlpM80hBQaU0goGIaXFBBo56UAJwKUcikpRxQA3vS4o96BmmIUHApKKOgpAJ1pQO9JS9qYCc0Zoo4NACU7oKQ8UmaACiiigQgopaM0hiUUYpaYhpopaSgBaQAmlpBmgBDSUppKAFoo6UlABRSU4UAIB60UtMI5oAO9OpKWgAzRScUGgQtJnNHSmdKBiUopDThgUAJSUppO1Ahwo70dqTNADqBSClHrQApNApKKAHA0080ooxQMBRS4pO9ABTTT8CkoAMikFFGKBBS0lFAAaSlPpSUAOoFNp1Awo4NBpKAG+1HSlpDQAtJRS0AJSEd6dRigCOgjtTsUCgREw44ppHFTEZpmD2oAhIppGKmIphz2pgQEetIR6VMRTdlIRCRTCKnK0zFAEBFMxVkjiottAmQEHrRUpB6U0g0xEQHFGKeRSYoFYZg0YNOIpO1AWGkUooPrQM4zQAZo6mjFFAC0Z9KKOM4oQg+tFBopgGaKKWkAUntS0lAw7UuO9JSjpQIMUlONNoAXvRxSUdaAQUUoooGKKcfemgelO6UAJzRzS80c0Af\\/1vS4hxzUxqGLpUhqDQKXvQKDQAuaSg+1LQAlIT6UtLwKAEBNFLTTQAtHWkApTxQAmaWkpKYhaQmlPvSUAApaQUtIBMUdKXikJwcGmAZptKaQUAFLRR0oEJRS0lABk0E0dKKADrSUvSkoAKKKT60ALSGjvSUAFJSikPtQIWlxTaTOTQMdSHPalpMUAIDRS9OKMUCFpppaSgBabnNLSYoGN4JxTulNHXNSGgQ00080ppAOc0DFpfrRRQIUUtIKXmgBaSgcmigYGiiigAzSe9BoFABRmjOaWgBKU0Yo9qAEozSk02gQppppTTaQCj1p4pnSnDkUxi0lHSjrQAU3mnUlAgFBooxQMBRmg0goAKMUtIaBCGkp1LQBGQM0hXinYooAiIxTSKkIpCBjFAiEjAppWpsUFaBlZlpu2rBAph6UCK5HamEd6n2000wICBTcVPtzTNtArEPtRipdtNwM0CsR0mOwqQikxzQAyjFOIxSAGgQgo96XGKTmgGHakzSnrRigAo70nelzQIDRS9aSgA4opaTOKACg0e9BGaAExxS44pOlLjIzQAYNJ0p1FAwHpTjTcYPFLznNAD91G6kyKMigD\\/\\/X9PQbU5qndTiNMmrWeK57VJvnVB+NQaGpp7tKjOTxnitHFU9OTbaKemeau0DCkNOppNAgooFHegQUlGTRQMKTrSmimAGm0p5o9qBAeBSUnOaWgBO\\/FLRSUAL0o6802nUCExRRz0pOaAFxSUtIfWgAzSUUvSgBDSmikNABmlJpB1oPWgGH0oApKWgANJxS02gBKBS0nakAtJSUtMQhpASOKVuKQYoGO60tJQKAENFFGOaACkNFNzmgQqjBzTjzSAUtADTQKGJ6UDpQA7tTaWgUCDFL2ope1AxBmnU2ndqBiUHFHSjigQ0+1FLSUDF4FKMZpMc0UALTO9P7UwCgBc0uaSjtQJiHmkFLRQMUindOKZnFO60CENOoxRQAnWjpSimmgA70tAooAQ0lLRjmgBe1JS02gYtJS0Y70CAjHWmmnHmkFADSPWkxTzSHpQAzgUmKfikxQAwjIphHFSn0pjCgCLFN285qXaOtJtoEQlcDioytWCKYRzQBFjApuKmIpmKAItuKZVjFMIHSmIiI9KMCpSKTbxzSEQkZpMVLtpNtMdiMim4qXbSbaBWI8EUuBin7aMcUCGYxxRinbaXBzmgBh9qbipCKTFAxg5p1KBRjnFAhtLRg5pcZoAZ70tKFpMUCEp3OKOKTvQMWil+Wj5aAP\\/\\/Q9MPArk7gtcXRA9cV0l7J5Nsz55rF0mF5Lnz3GVHNQao6WNBHGsa9hink0tJQAU3FOOKSgQnSl680Gk9qBBmjNJjmg+lMA70UhBBo5oGL0pO+aSl5oAKQUtIRQIKMUUUgADmlJo4FNpiCijNFABRQKU0DE4opKKBC0UClPtQAlJ9aKDQAmadSZGKKAFPSo6caSgAHrR1pOaUUAJjBpRikoPtQIRjzTQOaU9aQDmgB9JzmjHrSjmgBKQmlptAARnmk4pc02mA4UuaQHNBNIBtOU0maWgBTQKSgc0AOpaTFKBigAoFFJQAvFB55ooHJxQA2lpSOKSgANA4paQUALTaXNJQMQ0vakpQDigQlHSlpKAA04c0gANHTgUAOpDzSdsUo6UAJQaUUUAFJz2paTpQAhzS0nvS0AHQUgpx6UgoATmlFH1pM+lACmkpaQ0AFJig0ooASkp2aUgCgCPGTSECnUUAMIpuKlpCO1AERGaTFPxikIoAjK0hSpMelJjigCLFMK1NikYUAQ4pDzUuOOaTAoEQkc0mMVIVpMUARkUmOalx60YoER0hHHFS7RRtoCxCBSYIqXFGKYWIMd6MVNto247UCIwO9JjmpTSY5oGNxTSKl603rQIj2mk2A1LjPFGMdKAIttG2pdvFGKAsR7RRtFS4oxQM\\/\\/9HuNUnACwnnPUVPpcPlxFj36Vm3Ufn3hAOe1dEgCIqqOAKzNR9JnNJ1ozjimAppKWkFAhRRjmkFKT6UAJSe9OpKBCdaQ0ppKYBRR3xSUABNGeKUUhoAWkozmkNABRikHrT6BCYpaKQmkAh4pKOtFMAoopKAF+lLSUUAJS0YzSe1AC4o4pDxQKAA0UGkzQAZpM0tJQAUUYpaBDcd6AOaWigBTTPanGm0AJ2oyOlL1ppAoADQKaTnpS9OKAHcYoNAoPFADTmnUlLigApVHejtR0oAcOKKTNFABS4o680ZoAOtGBSZ70tAAaSg9aBQIOlB9qWk70DA0UhNFAC5xSUUlABRS02gBadTaKAFoozRmgBRRTaXNABRmkNFAC8UtN7UCgBxpKQ0ooAQ5pKU0cUAL1oNGaSgBBRS4pTigBO1JS0UAGOKTFL2ooAaTR2paMUAMxRjinGjFADcCmkVJTcUDIzSEU+gigRFikI7VKRxmkxQBEVpMVLSYoAjwKTAp+Oc0YzQA3ApMU7HNGBQIjxRin0YzQAzFGKfjtQRjgUAREUYqTFIRQBGR6UbakA4pcUCIsCl28U\\/FLjtQMjA4o2jGak20Y7GgCPFGKmwKMCmFj\\/\\/0u7jtX+2NIeg5rUzSUCoNR2aOtJRQIU4xQKKPpQAUhPpS57UgoEKeaTk0pNJmmMMYozRQM0AJSUUUCAUUdBTaAF9qPrRQaAAUUCloEJ2pKCaMYFACikozxRQAU4YpvSlHFACZoxSGigQHilFGKTpQMU0nGKSlxQAGm8UuaTHOaBBRRRQAd6UYphOKdQAuKQ0ZpDQAHpTc5p3WkHWgQGoyQOtLIe\\/pXO6hqDFvJgPPc0DNY3ESyeXu+b0q2vIya4mS0uUj+0Mcfzrp9MdmtlDEk+9AGlSEZpRSEkdaAF6HinUg6UtACUtFFACAZpaKB1oAKSlNQyzRwrukOBQBNSn2qrBcJcDcnQVY5oAWigUUABNJgGjFFAC4pKM80nfigBwFIeKWkNAAOaDRSUAL2pKKWgBKKdikxQAnSjFLSZoAKKWm0AOpuMUpoHvQIQ04Ck60UDDvRRim+1AC5o4zRigjFAC0UlFAB2paQUvfFABRSmigBKSlpM4oGJRQaXHFAhKQ0ppBQAlGKXFGMUMBMUwinnnikxQA3GKMZp2M0vQUARUu0Yp+KQg0gGYzSAU\\/pSEGmFiIg0CpO1IBigBCKbjnNSjmgigCOjAp2KMUAMxzSilxS8ChhYbjvSY5p+KMUANoxzmnUuKYhmKMU6igD\\/\\/0\\/TyKTpSk0hrM1FpM0fSimIWloGKQnNACZpRSUUxCmkpaSgAzRk0U3vQAvWk6Uo4oxmgBKUUGkoAKSlpMd6BAKXNNpQeaAFIpKWjPFIBKOtIaXNMAOKWko7UAJRRRzQAZpKXvRQAlKaTPNGaAEIpc4ooPNAgJzTaMc07gUAMpaKMc0wClPHNIeKaaQC5pM4ophPBPpQIzNTuvs8WO7dKztPtTK5ml6dRVO9uRdXZB+6vFdFGgtbYt6DJoYGZqD+YwiXnB5FblqnlxKp9KxbGM3NyZ3GQOfxroQMUDHUHmijHegA+tKT6Un1ooGLRzQKWgQlFFJmgArntYl5WIHrzXQHpmuV1Nw10V79BQI1tIyYCxGOa1etVbBAlogHGRmreOKLjClpMGloASkzRSUCCnYFNpaBhmkzSn0pKACilooASilxRQAUtJmigBPrRRnPFFACdqB70c0UAFLSUUAL0ozTaOe1ADqQ9aWkNAB70maSlPSgQUU2o5W2qWPamArzRxn5jiplZWGQa4SaeSedmYnk8V2FgpW2QMSTjvQxl3OetKT6U2g0hiUuKAKWgBuMUvakooEH1pMUtHemAlFLRn0pAIeBmm5yKdxSUAIMiilxSYoASjOeKDSUALimk44pw6UhoGNNJS0tAAKKKOtIBKXFLTST2piDnNIetFGOaBi0tFFACCloxRQIKKKKAP\\/\\/U9ONFFFQaBRS+1IKAClpKKACjpRRTAM5pKCe1JQId9aQ8UdaDQAlLSUUgCjvRRgUCEpTRSGmAhoHHNFBoAM0uc02igB3WjHFNpRQAoHrS00U6gBo4o70GigAPrQaOtLwaAGHPagZpaSgBaSjrSUCFFIaM0lAC5FGeabS0AKTTaKKAEIqhezeTbs\\/4VdbNc5q82dsQ47kUxFXTbfzZw79Bya0NTnDbYYzyTzT7P\\/R7MyN9RVezgN1c+bJzg5NIo17CHyrcZHJ5q+KNvpSigQDFLSUlAC0tJQeaACjPFBpcUANo7UlFMBrHC1w88hkvWIORu4rsbiTy4Xc9ga43T08+7AI680gO2g4iRfQVMKQDAxTqAEzmg0CloAbS0VXuJRDE0h6AZoET9aUVg2eptcXIjxwa3gc0DAnFJQaKYC0oxUJmjVxGTyamFIApDS02gBKdjim8U6gBKT2paKYCdKKDSZxQAv1pKTOeaAecUAOpQKBSZzSAD1opM0ooAYaQEmnmkI9KBCVR1KTy7ViOp4q6cCsLWZCI1QdzTBmVbRB5Bn1rtUUKoA7CuU0kCSUK3ODmuv4ApFCYwKSjNGaBC0ho6UGgBKKKXpQAmKM0e9FAxDRxilNGKBDcZpcYo5ox60wAdKSlpOlIBCOaOtB6UDpQAdKTGaXtQD6UANxQeKWkIoAQ8UoooPtQMDTT7U6koATBoFLiikAhoFGKOlMQpPek60h6UCgY6loopAf\\/1fTqbRmioNB1FFLmgBtFGOaXIoAMGkNKaQ0wA8UUdKM9qBBQaAaCaAE5ooBIoJoEFJRSCgBaKSloASlPSkNIelAEckqRjLnFVhfwdAwNQX9vPOuIqy4NIuADvPXtQCNwXsH96pBcxYzkc1jDSZQeelTf2ZKcAnigLGr9pg6bhSrcxscA9apf2agPB4q1HapGd3UjpSGWc5HFFL0oxTEJijoMUtIaAEJpKKBQIMUlLmg9KAG0UtIaADHNJS5pOpoAD7UUtIaBEbHiuPvJftF4dnOPl\\/KurndY42c9hXIwAFjMOpPSmNGpcyF0W2j6ADP1ras4BDCB\\/FjmsvTod7+a4zjpW8OKkbDNFLijFMBKM85FKM0GgQHBpKWk6UAB4opDS0wEpDS03ikBmarIUtGx34\\/OsbQlzcE+gqzr7\\/u1iHc5qfQotsbSMB6D1oYI6L6UhFFJQAnalwcUZpc0AMOazdUbFm49eK0Tx0rD1p9sAX1NMRn6OP8ASB+tdcBxXM6JGHZpT24rpqQxvNBOKXGOaQ9KBHI6s7\\/bQEbsK6m1LmFS\\/XFcjf5a+b9K62zBFsmeuKGPoWT602l6UgoAKU0lFAMDUUkixqXc4AqQms7UV3WrUCIptTiRcod3sKz\\/AO2nzjbzWLaLuuAufvGunOlRthh1oHYpf2tI3GME1Ml7N1HNXRp0Y5FTpZxqOlFwsUkvpc8ipV1DBw6mr628Y7UGGP0FAyKK4WToMVZGeopgRR0GKkANAhO+aKDR2oAjbBOa5XW3\\/fKPQdK6o1xeonzr5lPOKBdTZ0WIsfMxgYrpDxwaxdIDBCMcKMCtjkmgoMelJ3oziigQtJRRQAUUhzQKAFpD6UtIaAEo+lLRQAUhzRSigBKKKKACjGKWkoAQijgUUEUAN6milAo+tADaKXFFAxKSlFGM0CG0UuKOlAB0FJRjFLQAnak6Up6UnWgYtFNxRikB\\/9b0zjrSdTS0VBqHPSlwRRRmgQUUCigAzzS0lBpiEoxSilpAJ0FFIaUUwEpDSn2pKAYUgpaQmgAozSD1paBAajZgOtPNc\\/qs7xkKDihCNrzU6ZFSbx0FcMtzLI2Cc1cVLxzuMhGKBpHXeYO9HmJ6iucS2ujks2c96sxWUr\\/fzikNI1\\/PiJ4YcVKOeRVSKySNgx7Vd6CgBKKSjtTEKSMYFNopKBAaKMUoFADaWggCkxmgBKWiigBuKXNFJQIKSlpCcUDMjV5DHbHH8XFYlpCzsqj+KrWtyB3WMHkckVc0eEiLzG79KGCNeCIRRhFHFT0dBiigBRz0oNKBikoAKXtRxRQAlHaiigBtO7ZptL1oADTCe9LUchwpPpQI5LV5jJciMc46V02moFtFPc1xhla4vDIPXiu8tk8uBE9BQyuhPSUp6UlAhKTpS0lADDXL60wdwm7HHSuoY4FcNfSGW6YnqDimJbnQ6Gu23PuetbZNUtPTy7VAO4zTb8ziLMP14pFFwsO5pjMCOK5BZrrdnLc1Y827wTnpQJorTSCS9cjoGxXXxSIIlyw6VxVrA87F885zXRfY5GUFu9DHY1vOj9RTgQeRVKOyQcvk+1XFjVBhaLiHUnNOpDQIOKzNTIW1atI9KwNZnEcYTuaBmFp5BuUGP4q7sDAxXJ6RCXmVtvC85rru1ACUd6Kjd1jXcxxQBLSGo4pUlGUINSUCE70pox3ooGJSd6KCKBIY3ANcHN8127A55613Mx2oT6CuChOZs+poH1O40v8A49QfU1o1Vsk2WyL7Zq3QMaaQ0Gkye9ABQaX3pKBCUtApaBiZpKOtBoEJS0tJQAlFFLQAlGKSnUxic0dKWg0hDRS0UUAJiilxSMKADtSAUtJ0oATFFFLQAnSm804000AFFFJQAE0gpcd6WgBMUYp26jcKQz\\/\\/1\\/TO1AptKKg0HUmaM0negBaWkzjpSUAOoFFFMQnelo+lFIA70mKUkUmaYCUUUUAFGKSlHTNACUUopMUAJUUlvDKMSKG+tTYp2KBFeO2gjGEQAfSpfKjxjaKeKKQxFVcYAxTqTNFAB2ooooENopaSmAlFOpooEGKd0pp60hoGB5o60UhJFAgHWl4pvfml60AJQPegelBwBQIDVK7uBBGX9KnkkCLk1y93KbuT5c8flTAz5JmlmMh65rsbJAkCgd+a5GGH\\/SgvuK7dBhQMYpdShScc1h3GpmO68tRwOtbEzBUJPauP2tJcmQnPOaYjsRKm0MTxUkcqSD5a5e4knkj3g4C+lWtJmbeUc5LdKQI6HvS5ooFABnimUpbBxS89qAEHSg+lLSUANNUL+YxWzleTjHNX2rntdl2xLH60xGRpkYkmAIzk813gx0FcnoMBMplbsOK6zpSKFNNpaSgBKO1HNIaBFW6k2Qs3oK4qNTc3AB6k102sSlLfYvVjz9KzNFtxJP5p7UwR1UaBEC+gp2M0oFL0pDIDBEedoqhqQSGzdlHOOK1c1ga1IfIWNTgk0CKujwBnVm7c11WKwtFT5C57cVu80hthjjimmnE1BM2yMt7UxMxrzWBbyGONd2Op96u2N8LuPcRg9xXI+UZ7k89TVmQT6fNuAORTCx2TMFGSa4y+drm4OeRnAq5cav50OyMYJ61Bpto1xIGb7q80Ab+mQeTbgnvzWl70ijaoHpSjpSAKyNXjke2\\/d\\/j9K16jlGVNAHHadI8Fwrdjwa7ZdpGRXGDHnsMV10HEK\\/SgdiU0lKaKBDT1ozS0h9qAM7UJGS2cg44rj7NTJJxySa6TW5NloRnqcVj6Ou6UDpzSYI7SIbIlUdhU2ajAIbHank4pjEIooByKSgBccUnNLRQAlBNHSigAzSGlxR1oEFIeuKdnjFNoAOlFJS0AIRRRRQACl602igBRRyaTNLQAnQ0uaSigBKBTqTFMQlKaKKQxuOKMUH2pTQA0mkpetJigBe1NNO7UmM0AJxRxS4oxQM\\/\\/0PSxRRRUGgUUvWkPpQA7NJSUUCFpabmlpgL2pKKQnNAC4pKDS0gEpO1LijpTASge9FLQAUUUtIQmKKB1pelMAFFJSigbA0maD1pcetAgBzRRSGgBDRRR1oAWm0tGaAENFFIWC9aBCjrSEjPFVy7Odq9PWpgABigAo60dKM0AHSmO2ATSSSBBk1z15ftP+6h496AG3l01yfKi6A\\/nUyQG1tWkYfNjPNWLGxMeJpeT6UasxEHy9+tG4MztMQyz7z25JrqK5\\/SQsaFz0NbytuG6gbMzVJvLgKnq3Fc9axtK5cGrutzb3WH0qzpNr+7Dv06gU2C7liaHyrNifSszSnAuVA75rd1HItGx6VhaQjfaFcjGKQI681FI4UVKay2dproIv3R1oEXos43HvUopcCk6GgANJR1peKAYxq43VZ2lujEcYXpXZMcAk1wkn7+8YjHLUAdZo8SpbZHOa0upqG2Xy4FTocVPQhvcKKM0UAIaYaeabQJnMa05MgAPQVa0SErEZD1JrM1N0NyytxjFdLp6Klqm3uM0DS0LtNpx60UCG1zmsENMqdwK6Q1h3kDSXS8ZBxQNF3TozDbgHvzV\\/NMVQihfSnUCFqleyLHbuT6VbxWVqh\\/0cigRz9ijSXS4HfNdjJDFMm2RQRXNaOn7\\/wAw11Q60FGOdGt9+e3pWlHGkQ2xqAPap6SgQlFFISMZoAKqXkyxQMxPsKzrvV0t5fLC5x1NYl1qD3jBcYANOwFi2LSzYxnNdgi7UA9BWJpdsuPNNbhI6UhgKU9KYWA604MGXIoASkpTTSaCTldfc5ROxzSaKhaVR6Gq+svvuwg5ArY0RF5IHIFBSOi7Uwjmnk4FNzQAlFFNzzQA4UGkFB60ABopaTigQnNLSUUAFGaWmnrQAtFFFACUUUUCDFJTqT2oGJmijFB6UwDHFKKSlpAHFJS4pOtACfSilAxSEUwCm+1OpO9ABSYp1GM0gE47UntS4xSUAFFLRxQM\\/9H0rGOtLTM5pc1BoKaOtJmlzQAtLTQaWgBKWkpaYgo70dqBQAUtITS5FAASKTGaKKBC8UEYptOHPWgAooGKDQAlGc9aBSmgAxSU7tSDpQA2nUnPejNABSUtIaAEpRRRQAEYptO6VC7BF3HgCgQSypEu5zgCspZZb6Qqnyxjr71CzG\\/nCA\\/IOa2oo1iUKgwBTAcihFCjtTqM00nFIBTTHdY1LN0FVLm+ggUktz6DrWJJPdXjAIp2+lMBby+knby4Bx61esLALiST61NZWIi+dxz2rU20rjDovFZeoQmW3O3qK1NuaaV7GhCOWtZfKiMZ4Oa6RM+UMelRfYoA+\\/bzVsDjFAzkJ7eaW9ZSvJP6V1VvCIYlQdhUpjXO7HPrThQwM\\/UuLR\\/WsXSW2zBW610V3F5kDKBkkVzNpvikB4yvrQxo6K8n8uMgdSKbp8RWLzG6tVJIZbqTLnittRtUKO1Ah1MPNOHNFAgFNNO4ppoAq3b7Ld29BXH2Sb7hc85NdHqzhLY5PXisjRVL3AOOAKAR14AxRS9qKAEo7UUUAHNNbgU6kbkYoA4rUNrXTH+InpXXWihbdAPSsa9sGZ\\/MTmti1LiFRIMEUDLXWm0ZoNAgNN2jOfSnUYoATNJml6CkoAU8isXVXVIwWraNZWpqrRZYdKAKejAbi3UV0Q9a5zRzh2T8q6Me9AMKKSloAKaQCKdQKBHP32jrcHehwazV0meLgj8q7HFGBQUc3HHNGBt4NXd103A5rW2J6CnbQOlAFOOKTgyGrYwBgU7FNoEFMb7pNOJqC4fZEzjsCaBHDXb+ZfM3viuu0lAsJx3ri0\\/eXBJ7mu+sU2Wy\\/SgotmjjFFFACYpDxTjSEZFACCl70n0pxoEIeKYOTS0ds0ALRigUdqAEoopKAFozR1pDQAuaSlFHtQAlAFApaAENJ1oooEGKKKKAHZptFAPrQMM0UmaAaBBiig0ZpjDHal7UnvS0hCU3pTuppG9KAF4o4ptFMdz\\/0vRxz0oOc1ladfG4yj\\/eHNa3Oag0DpSilooADQKDQKBC8Uh5NAoxTAdSUUDrSAMUUtJ3pgGKTBpaWgQlLmkoFABRR3peKQAKSlpKYCmiiigBDQKTHNL2pAJ1oNFHWmAClOKTNIfagArJ1MyeThDj3rVxTGRXG1hkGgRzOnXEdtkS9T3raW\\/t3+644qvNpMbsWjOD6VB\\/ZGOn40DZYl1OCNcg5+lZcuo3NydsI2g1pJpcan5jkGr0VpBCMKv4mi4GBBpc0x3yHnPJNdHDAkKBVHSpelLQAlLRRQIKSlNNzQAtIOaO9LmgBeaQUnWnD0oADyKqtaQO24rz7VbpKBiKioMKMUvWlooATpSE0UnSgQUZzRSGgDnddkIRUH1qTQ4lEbSdzxVLWyTMoJ7Vs6SALUUMaNWiik4oATml5paSgApOtKeKQCgQYpO9BooAKCaWmmgAooxS0xB1oANLRSGGKo3yb7dhjNXaa6hxtPSgDnNNOy4wx9hXTCuYktJbe4ynTORW5bNM65kGKBsuCkNIKCaBBSjpSCnfSgBKKWk7UAFLRQKADNJRSUAIao3rhLeQtwMVeNZOrEC2IJAz60COWsV3XAyOpxXoEY2xhfQVxWlR7rlQRnByK7jrwKChAaKPpRjvQAGm0p5NFIQUUmKSmAtFBNNJoGKTRmkpB15oELRRTSPmBoAf0oyM80ntRigBfakopSKAEpeKSk4oAD7UUUmaAFyKSilxQAlFLnFJTAQjNKKO1NoEOzSUCkoGOzxQtNzTx0oEJ3oNHTpSe1ACZFHFLxRxQM\\/\\/09+0PlXYI6dDXVVy8QDXi7RxntXUVmaDs0UgopgLSUUvXigAHTFL0o9qSgQGgUUoxQAGkooxQAZpOTS0tMBOaQUpNHSgQpGKSkyelLigApKKKAFFLSUlAC0GimmgBeaTFLmkoAKWkHpSkUCEpppaKAEHvTqSimAtJRQeaQBil4pB0ooAX3ptOpvSgAzmkxS0UAHAoIyKXFJz2oAOKXkU0U6gANFFAGaACndajxzTqADFN5p1J2oASjFGKKYzH1DTftREiHDDir9pbi2iEecmrQFBpALSUmaBQIdSUtJQAUtJRwKAExSUoNIaYB70tJS0ABoFIeaWkAGloAoxQAUlHSkoATap6inAUUtACGkpc5oNACUZoxRigAzS4opelACYpKU0lAC9KSikNACmsDWz+5C9cmt41zetFldVHcZoBEejoRKAemM11YrB0UZQuR04re4zSGwoo6UnWmAUUh4pRQIbRRSUAKcdqSlooAOtJRRQAUUc0UAFApO9LQAvFITSUGgA60fWig0wCijrzSUCDPNLk0n0pfrSATNFBo7UABpDQaQ80AKDg0GijNMApetGaM0AGKQmijPFAC8UcU3NGaAP\\/9TpdPTfd7h0HNdHWXpcJWMyn+LgVq1magBxS4wOKD0pPamIOtL9KSlFAhevNFFFAC0mKKKAA0E0lHNMQGlpvPeloAM0AZpe1KKAEowaKKBiGjFLRQIM0lKabQA403FLjvSUALSUtBoAMetNOTxS0d6BCY9aXFFHWgBKQcUpNHBHFABRRS4oAbSjFBpOlAC5zSHrSgUGmAmOaWjrRSAKTFLRQAYHWiiigAopTSUAIaUe9FIM0wFNFJSmkAlAFLjijjFABSGikoAXiijFGKACiiigAxSGnHmm0AJRg96KWgLCUuKO1GaYABS8YpM4pM5pAOozikpaAEPNJS0AUAFIadSUAAopKWgBOaWjrRQAUGjtSUAFFB6UCgAoxR2ozjmgArl9Zc+cmB04rp81zGrA+eMdKANXSVxbA+tatU7JBHbqB6VbNACmkHSijpQAlL2pKSgAooooAX3pM0tIaAEo70Ud6ACkNLSEUAIDTs0goPTigAxmlpBkcUtADTRmlIoxxQAlFOpCKBAKTnNLSHFABRRijFABSUppKYBRRRQAvFNpaKAFGKaRzS0d6QBRRRQB\\/9X0cAKNo6CnDmm0tQaC0UCjPagApSc0YzRj0oAM0UUhpiHUUgNGSelAC0hOBQaKBCduaWkNLQAZpabS49aAFozRiikAUUUfWmMQ0YozSGgQ4nikpBS5oAWmk0p9aSgAFFFFAARR05ozSUCFNJRRQAcdaXJpKKBinmkopKYh1IaTNFIBRxSikpaBiGilxSCgQYoxzRRmgBabS0UAFB4FJQaACg0UuaBhTaWigQg60tAooAU0lFJQAtFJS0DCgA0lLuoEJRRRQAUUUAUwG0DmlpRSAKKKKACjNFGKAClpvSnUAIaKKKAA5owaKKAEpaQ0UAFHSlPFJ1oAKKKSgAxmsC5j8282Y6Gt8VAYAZ\\/N74oGToNqgU+mjiloEBpBS44ptACmijNKaAG9aMUUUALSGjrRQAnakxTjxSUAFFIKXIoABRRmigAxRQaKAENHajNFAmFHUUd6UnigY0UlLRQIKWmiloGHNN5p1J1piEpcd6MYooATFA6U45xSYoAKKMUlAC4oxRRQM\\/\\/W9HJoBycUHFIOKg0H57UlBxR1oABS0lFAC9KTrRzS0xBjilzRRSASiiimAClpBxTjigBB60uaOtJQAZ5wKWkAozzQIU0dqaeTmlNADaWikoAXFL0oBxSdaAF60hpw4FNoEFHNFJQMXFIacORTaBBSUUtAABxQKQUUxi96Q+lFJQAopaKAaQgoooFAC03pTqSgApD1oPtRigBaBRQKYBRgU3PpRzSAdSCjmkBOOaAH4pKOaKAEpaSjmgYGkNLSGgQUmaKQ0ALmkooyKACikpaADNO7U2l5oAUUtJS0DA0lLRmgQlFBpKAF60opop1ACUUvSkoAKKSnYoASjpSikoATrS0lFACGilxS0AJRS0lAAaWjrSUDF602nUlAg4AzSdaWgUAGKSlpKACiiigBOtKBSUUCCiikzTGJSjNFFAC0UlHNIQh9KQUvPejGRTGFLSD0pTikAUlLSZoEJ16U6kxijpQAlAFKR3pKYC5pvelzQRxQAo55FIaUHAwKSgA60GgGgUALRTuKOKAP\\/9f0Y8Ug5NFLUGgvWlpKM0ALmlHSm8dKOaAFp3amiloAKUUYpcUCE70GlpM0wEoFLSUAGcdKWkpTQIKSlJooASiiigAooooASilpPegBc8UmadTaBB1ozRQaADrSUopMUAFKKDSZ7UALikxxS0UwE6CgetLRSAQ0oFJiloABzS+1NGKWgAo6UlFACjrSmkoz2oAQ0tN60vNABRRS0AFBopKAAGlzSCigAo7UUUAHSko60UAJSUppKAEpBS0uKAEpaTFLQACl4pMUUAP4pMmkpwxQAUhpc02gApabS0wClNAopAFFFLmgBven802lNABSUtJQAlFLSUAFL1pKUUAJRS9DRjmgBKKWkoAKKKQ0ALSc0UnvQAvakpaKAFpKKSgQUUUlABQfSj3opjCgD1pcUE9qQhMUtNzRmmAtFNPtS0AFLSUcUgAUAUoooAKKBSUwDNJQaCKQgxS4FJSimAUh6UdKdxigY0cUUppM4oELmjNGRRkUDP\\/Q9G6Umc0daKg0HH2pKSjNAD6Qe9AozQDFoFJ3p1AhaWmg4paACkGTS0gz3pgKaT60CigApaDRQAlJ0pc0lAg7UmaUCj2oAKU0lLQAUlFFABRSGloELTetLRQAtJR1ooAKTGKKWgAooooAWigUlAwoopM0CFpDR1pBxQApopOKKAFzRQKQigBaCaUdOaSgBDS9qQmlBoAKKMigHAzQAUUZzQaACik60uMUAGabTqaKACkp1JimAUHiiikAlApaWgBKKKWgAzSdqKXtQA3vS9aOnNN3j+LigB2KUYpgbJp1MB1NopcUgEopaDQAZopBS0AIfSjpS5FJQAo5FNNLmk60AL1paToKM0AOPtSUmaKAEopaSmAUGig0gCkoooAXOKTmjvRTAKKKKQgooHFFACYxSUpo470wFpMUoopANpeKKOtMANA4HNBoxSAKTijp0peKYCZoBxS9aQ0AJSmkFBoAM0A0lFAC5pabSjk0AFFHencUAxppBTsetJ0oAWlpM0ZoA\\/\\/R9F70maSjPaoNB2c0lFFAAM06kHTinUALSE9qTNKo70AKDS5oxSUxC0ZoOaKACjPrSUY5oEOpKSloATkmlNJnBpRQMSikpcUCA0lKaaaAHZopB0oxQAtGe1NpaAFoPpQKKADFFJS0AHSgUUdKBIMUtNzRQMWgA5pBRQIcTTcc0tFABTaWkoAMUtJS0AFJTuDTKBi5NH1oooEHWlFJ1pT6UAHeg0A0h9aADpR1NFFAC0UUnegApabTqAG0tFFAB2pKXtRQAYpKcKTFAABzRS0GgBKTmgUtABSEZ606kPWgBuAOlLRS4oAQUopM0ZoAdmkoFIfSgApabTqACkpaSgANL2pKKAFpDRmlNADTS0UUAJRS0UAIDmkyKd0puKBAaKWkoGFGaKSgBaDSZpe1AgopKQ8UDFxk0EUdqKBAtFFBxQAlKKD0oPFMBKXNNBNLQAlBoz60nWgB1Jz2o70vTmkAE0lGaKYAKKKKADHFGKQ8UUAFO96QUGgAFKaAKXtSAZzRzS0Uxn\\/\\/0vQSce9OAoFFQaC0daYafnjFACjgUUlLmgAzzil+lIKd7UALmkHrRx3pR0piFpDQeKSgBRS0CjFACUGiigQmD3p2KbQT2oGO6U3POKSigQUlKaPpQA7oKTPakzRQAE0UUUwDOKUdaSlBpAGaXtTT7UCgBetBopaBCGkpTSUALRntSUd80DFpKCMCgc0AKRR0o6dKDzzQAlL2o7UdBQIOlGM0lH0oGBpSMUmKKAFpMilFITmgQtJmjoM0UAFH0ooFAC9uaTNBNA5oAQ0ZooNACig0A0lAC0Uc0tACUUppKADNLTe9AoADRmg80mKAFzRikpR0oAWjNFJQAUUnenUAFJS0lAB3paSigBc0lJRQAtFKBSHigANFIKM0ALRSUUALS0lJQAHmjpRmjHegQlFFIaAFoopKYIOtGaBxRQAUmCaUGjIpAJ7UDrS0negB1JRQaYxKCcmjmigQneloz6UUAIRxmiiigAxQKXNFAAaQUGgUAHIoApfaigBDR0paQ5oAB6UAUUmc0ALzSnpmk6ijrQAZFGRSYpaAP\\/\\/T9CHrRR0FJUGo8CjFJnijOaBCmgcdKOKM0ALmlpM4ooAXrS57U2lpiFNFAPNFABk0ZoooEB5ozRSGgBwIpKBilFAxp4p2KZ1peaBBRRiigA47UuKTNGcmgBKXrRSigBCKOBS0mKAF60e1IM5paAF4o+lIT6Uo4oAQ5o60ZzRmgApTTaXNAB1pBS0gPrQAE0UlOoAXtTaCeKTNAheKWm0tAw4ooo70CF600U6m0AKelFJS9qACkNH0pKAFFBpKXHGaACl7U0c0vSgAozSZNFADs0E0gpKAFopM0tACUtFJQAe9LRRQAUe1LSUALim0uaTNADqCaTNBoAM0ZpaSgAoooNMApM0tNNIB3SjrTaKBDqTvRiimMXiko7UUgCkoopiF6daTNBopAAooooAKSigUwFpCaQ0UALRScUnegBaKDx0pM0AhaOaOgozQAZpOtH1pRQAgzS5peKbikAUtJiimIU0lLSDmkMSlo6UZpgBpRSHJo6UAJk0tLnmkoAKSlpRQAgoopKAEzRmiigD\\/1PQvrRmkoWoNQOacKDSUCFpKKBQIcKM0UhoAWlpBS0wFJoFJS9qADvS0lIaAHUYzS0lABR3o7UlAhcc0lKabQAtHFB6UCgAo7UtNoAUUopKWgAxR9aSigAJpO2aKd2oATNGaKO9ABmig0GgAxRjinDpRQAykp1IOtABS0h60UCF7UgxR2oFAxTjtSUU5aBCUCkNAoAM0ZopKAFxS02loGFHSlptAgHWj2oooAXpSUGigApcUUGgBKSiigApc0UlAC0UlKKYBRRSjpQIXtTKWkpDFoo70poAQdaWgUlAgoFFJQAuaU02imMXNFJ2paQhKWgdKKYBRQ3SkFIBxpuaWkoGFFB6UUxAaSlpO9AC0UUdqAEpDzS0hoAbTu1KOtBoAbS0UhoAOtLxSDrQaAFozSUGgQdqUUvagUDEpTTTSikAtNPWlNJTAM0ZxTTSikICaKU9aKYxB70pNNpaBDqbS0nagYoxTs8U3tR2oADijHFFAoAMUYpaKBn\\/\\/2Q==\",\"formats\":{\"latex_confidence_rate_threshold\":0.5,\"latex_confidence_threshold\":0,\"wolfram\":\"true\"}}' \
    $'https://api.mathpix.com/v3/latex'

    -b $'mp_cc2c06325cdadd9d44035495d5225d52_mixpanel=%7B%22distinct_id%22%3A%20%221680a03537e37-0c7155d8a71a02-285e3568-2c600-1680a03537f7ea%22%2C%22%24device_id%22%3A%20%22167cf4c90fa3d-04241b0cc73ceb-285e3568-2c600-167cf4c90fcdb%22%2C%22%24user_id%22%3A%20%22%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D' \
    -H $'Connection: close' \
    -H $'Accept: */*' \
    -H $'Accept-Language: zh-tw' \
    -H $'Content-Length: 21513' \
    -H $'Accept-Encoding: gzip, deflate' \
    -H $'Cookie: mp_cc2c06325cdadd9d44035495d5225d52_mixpanel=%7B%22distinct_id%22%3A%20%221680a03537e37-0c7155d8a71a02-285e3568-2c600-1680a03537f7ea%22%2C%22%24device_id%22%3A%20%22167cf4c90fa3d-04241b0cc73ceb-285e3568-2c600-167cf4c90fcdb%22%2C%22%24user_id%22%3A%20%22%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D'


{
   "metadata":{
      "count":17,
      "mode":"solver",
      "user_id":"16E45C4A-46F7-4F94-A95F-EDBF8F463941"
   },
   "url": "data:image/jpeg;base64,<base64 encoded string>",
   "formats":{
      "latex_confidence_rate_threshold":0.5,
      "latex_confidence_threshold":0,
      "wolfram":"true"
   }
}


'''
