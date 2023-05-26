import requests as rq
import json
import pandas as pd
import numpy as np

# Imita um navegador para passar restricoes
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
headers = {'User-Agent': user_agent}

vFinalPage = 999

vPage = 56
vTransacao = 'aluguel'
vCidade = 'fortaleza'
vPrecoMin = 150
vPrecoMax = 950000

vUF = 'ce'

vImvl = "studio"

vBASE_URL = f'https://www.zapimoveis.com.br/{vTransacao}/{vImvl}'

dfs = {}

while vPage <= vFinalPage:
    
    vURL = vBASE_URL + '/?pagina=' + str(vPage) + f'&precoMaximo={vPrecoMax}&precoMinimo={vPrecoMin}' + "&tipoAluguel=Mensal"
    
    vResp = rq.get(vURL, headers=headers)
    vStatus = vResp.status_code

    if vStatus == 200:
        vHTML = vResp.text
        vHTML = str(vHTML)
        
        vValPag = 'NOK' if 'Não encontramos resultados' in vHTML else 'OK'
        
        if vValPag == "OK":
            if '"results":{"listings":[' in vHTML:
                vHTML = vHTML.split('"results":{"listings":[', 1)[1]
                vHTML = vHTML.split('],"superPremiumListings"', 1)[0]
                
                v1 = '{"listings":[' + vHTML + ']}'
                v1 = v1.replace('R$ ','')
                
                j = json.loads(v1)
                
                # f = open("html.txt", "w")
                # f.write(vHTML)
                # f.close()
                
                df = pd.json_normalize(j['listings'])
            
                # df = df[['type','link.href','account.name','listing.usableAreas','listing.totalAreas','listing.title','listing.description','listing.createdAt','listing.updatedAt','listing.floors',
                #             'listing.parkingSpaces','listing.address.zipCode','listing.address.point.lat', 'listing.address.point.lon','listing.address.street','listing.address.neighborhood','listing.address.streetNumber','listing.suites',
                #             'listing.bathrooms','listing.bedrooms','listing.advertiserContact.phones','listing.whatsappNumber','listing.pricingInfo.salePrice','listing.pricingInfo.yearlyIptu',
                #             'listing.pricingInfo.monthlyCondoFee','listing.publicationType','listing.unitTypes','listing.unitSubTypes','listing.usageTypes','listing.amenities']]
                
                try:
                    df = df[[
                                        'account.name',
                                        'listing.acceptExchange',
                                        'listing.address.city',
                                        'listing.address.confidence',
                                        'listing.address.country',
                                        'listing.address.level',
                                        'listing.address.neighborhood',
                                        'listing.address.point.lat',
                                        'listing.address.point.lon',
                                        'listing.address.point.source',
                                        'listing.address.precision',
                                        'listing.address.state',
                                        'listing.address.street',
                                        'listing.address.streetNumber',
                                        'listing.address.zipCode',
                                        'listing.address.zone',
                                        'listing.advertiserId',
                                        'listing.amenities',
                                        'listing.bathrooms',
                                        'listing.bedrooms',
                                        'listing.businessTypeContext',
                                        'listing.createdAt',
                                        'listing.description',
                                        'listing.displayAddressType',
                                        'listing.externalId',
                                        'listing.floors',
                                        'listing.id',
                                        'listing.isInactive',
                                        'listing.legacyId',
                                        'listing.link',
                                        'listing.listingType',
                                        'listing.parkingSpaces',
                                        'listing.portal',
                                        'listing.preview',
                                        'listing.pricingInfo.businessLabel',
                                        'listing.pricingInfo.businessType',
                                        'listing.pricingInfo.isRent',
                                        'listing.pricingInfo.isSale',
                                        'listing.pricingInfo.monthlyCondoFee',
                                        'listing.pricingInfo.period',
                                        'listing.pricingInfo.price',
                                        'listing.pricingInfo.rentalPrice',
                                        'listing.pricingInfo.rentalTotalPrice',
                                        # 'listing.pricingInfo.salePrice',
                                        'listing.pricingInfo.yearlyIptu',
                                        'listing.propertyType',
                                        'listing.publicationType',
                                        'listing.subtitle',
                                        'listing.suites',
                                        'listing.title',
                                        'listing.totalAreas',
                                        'listing.unitFloor',
                                        'listing.unitSubTypes',
                                        'listing.unitTypes',
                                        'listing.unitsOnTheFloor',
                                        'listing.updatedAt',
                                        'listing.usableAreas',
                                        'listing.usageTypes',
                                        'type']]
                    
                    #Insere a coluna com o tipo de imovel
                    df['imvl_type'] = vImvl
                        
                    #Tratamento dos dados
                    df['listing.publicationType'] = df['listing.publicationType'].fillna('Standard')
                    df['listing.address.point.lat'] = df['listing.address.point.lat'].fillna(np.nan)
                    df['listing.address.point.lon'] = df['listing.address.point.lon'].fillna(np.nan)
                    df['listing.address.point.source'] = df['listing.address.point.source'].fillna('')
            
                    # Remove colchetes das colunas
                    df['listing.floors'] = [''.join(map(str, l)) for l in df['listing.floors']]
                    df['listing.unitTypes'] = [''.join(map(str, l)) for l in df['listing.unitTypes']]
                    df['listing.unitSubTypes'] = ['|'.join(map(str, l)) for l in df['listing.unitSubTypes']]
                    df['listing.parkingSpaces'] = [''.join(map(str, l)) for l in df['listing.parkingSpaces']]
                    df['listing.suites'] = [''.join(map(str, l)) for l in df['listing.suites']]
                    df['listing.bathrooms'] = [''.join(map(str, l)) for l in df['listing.bathrooms']]
                    df['listing.usageTypes'] = ['|'.join(map(str, l)) for l in df['listing.usageTypes']]
                    df['listing.totalAreas'] = [''.join(map(str, l)) for l in df['listing.totalAreas']]
                    df['listing.bedrooms'] = [''.join(map(str, l)) for l in df['listing.bedrooms']]
                    df['listing.amenities'] = ['|'.join(map(str, l)) for l in df['listing.amenities']]
                    df['listing.usableAreas'] = [''.join(map(str, l)) for l in df['listing.usableAreas']]
                    
                    # Cria colunas baseadas na coluna listing.amenities
                    df['listing.pool'] = df['listing.amenities'].map(lambda x: 'True' if 'POOL' in x else 'False')                   #Piscina sim ou nao
                    df['listing.sauna'] = df['listing.amenities'].map(lambda x: 'True' if 'SAUNA' in x else 'False')                 #Sauna sim ou nao
                    df['listing.backyard'] = df['listing.amenities'].map(lambda x: 'True' if 'BACKYARD' in x else 'False')           #Quintal sim ou nao
                    df['listing.garden'] = df['listing.amenities'].map(lambda x: 'True' if 'GARDEN' in x else 'False')               #Jardim sim ou nao
                    df['listing.barbgrill'] = df['listing.amenities'].map(lambda x: 'True' if 'BARBECUE_GRILL' in x else 'False')    #Churrasqueira sim ou nao
                    df['listing.partyhall'] = df['listing.amenities'].map(lambda x: 'True' if 'PARTY_HALL' in x else 'False')        #Salao de festas sim ou nao
                    df['listing.tenniscourt'] = df['listing.amenities'].map(lambda x: 'True' if 'TENNIS_COURT' in x else 'False')    #Quadra de Tennis sim ou nao
                    df['listing.sportcourt'] = df['listing.amenities'].map(lambda x: 'True' if 'SPORTS_COURT' in x else 'False')     #Quadra de Esportes sim ou nao
                    df['listing.bathtub'] = df['listing.amenities'].map(lambda x: 'True' if 'BATHTUB' in x else 'False')             #Banheira sim ou nao
                    df['listing.soundproofing'] = df['listing.amenities'].map(lambda x: 'True' if 'SOUNDPROOFING' in x else 'False') #Prova de som sim ou nao
                    df['listing.fireplace'] = df['listing.amenities'].map(lambda x: 'True' if 'FIREPLACE' in x else 'False')         #Lareira sim ou nao
                    df['listing.gym'] = df['listing.amenities'].map(lambda x: 'True' if 'GYM' in x else 'False')                     #Academia sim ou nao
                    df['listing.hottub'] = df['listing.amenities'].map(lambda x: 'True' if 'HOT_TUB' in x else 'False')              #Hidromassagem sim ou nao
                    df['listing.furnished'] = df['listing.amenities'].map(lambda x: 'True' if 'FURNISHED' in x else 'False')         #Mobiliado sim ou nao
                    df['listing.guestpark'] = df['listing.amenities'].map(lambda x: 'True' if 'GUEST_PARKING' in x else 'False')     #Estacionamento Visitantes sim ou nao
                    df['listing.playground'] = df['listing.amenities'].map(lambda x: 'True' if 'PLAYGROUND' in x else 'False')       #Playground sim ou nao
                    df['listing.mountainview'] = df['listing.amenities'].map(lambda x: 'True' if 'MOUNTAIN_VIEW' in x else 'False')  #Vista da montanha sim ou nao

                    dfs['df_' + str(vPage)] = df
                    
                    print(vPage)
                    print(vURL)
                    vPage += 1
                except:
                    print("except")
                    break
                
        else:
            print("erro")
            break
        
    else:    
        print(vURL)   
        print('Erro ' + str(vStatus))
        break
    
vListaFinal = []

for i in dfs:
    vListaFinal.append(dfs[i])

df_final = pd.concat(vListaFinal, sort=False)

print("Criando CSV")
df_final.to_csv(f'./data_to_join/dataZapImoveis_{vTransacao}_{vImvl}_{vPage}TODOS.csv', sep=';', index=False)
print("CSV Criado")
