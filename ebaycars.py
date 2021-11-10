'''Guided Project: Exploring eBay Car Sales Data by Vinicius Malafaya'''
# Importando as bibliotecas
import pandas as pd

# Lendo o arquivo .csv
autos = pd.read_csv('autos.csv', encoding='Latin-1')

# Renomeando colunas para snakecase e fazendo ajustes para melhor entendimento
autos.columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price',
                 'ab_test', 'vehicle_type', 'registration_year', 'gearbox',
                 'power_ps', 'model', 'odometer', 'registration_month',
                 'fuel_type', 'brand', 'unrepaired_damage', 'ad_created',
                 'num_photos', 'postal_code', 'last_seen']

# Removendo coluna com valores '0', e outras duas com muitos valores repetidos
autos = autos.drop(["num_photos", "seller", "offer_type"], axis=1)

# Ajustes para ver 'price' como um 'int'
autos["price"] = (autos["price"].str.replace("$", "")
                  .str.replace(",", "").astype(int))

# Ajustes na variável do odometro
autos["odometer"] = (autos["odometer"].str.replace("km", "")
                     .str.replace(",", "").astype(int))
autos.rename({"odometer": "odometer_km"}, axis=1, inplace=True)

# Removendo registros com valores de ano de registro inválidos
autos = autos[autos["registration_year"].between(1900, 2016)]

# Analise de kilometragem e preço médio das "top 10" marcas anunciadas
common_brands = autos["brand"].value_counts(normalize=True).nlargest(10).index

# Analise precos
brand_mean_prices = {}

for brand in common_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_price = brand_only["price"].mean()
    brand_mean_prices[brand] = int(mean_price)

mean_prices = pd.Series(brand_mean_prices).sort_values(ascending=False)

# Analise kilometragem
brand_mean_mileage = {}

for brand in common_brands:
    brand_only = autos[autos["brand"] == brand]
    mean_mileage = brand_only["odometer_km"].mean()
    brand_mean_mileage[brand] = int(mean_mileage)

mean_mileage = pd.Series(brand_mean_mileage).sort_values(ascending=False)

# Dataframe final
brand_info = pd.DataFrame(mean_mileage, columns=['mean_mileage'])
brand_info["mean_price"] = mean_prices

print(brand_info)
