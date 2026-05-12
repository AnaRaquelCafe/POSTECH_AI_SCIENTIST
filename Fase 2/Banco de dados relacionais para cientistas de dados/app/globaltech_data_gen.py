from core.config import Config
from pandas import DataFrame
from faker import Faker
import random
from rich.progress import track
from sqlalchemy import create_engine

fake = Faker('pt_BR')

class GlobalTechDataGen(Config):
    def __init__(self, n_clientes=100, n_produtos=20, n_pedidos=500):
        self.n_clientes = n_clientes
        self.n_produtos = n_produtos
        self.n_pedidos = n_pedidos
        self.engine = create_engine(f'mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}')

    def gerar_dados_clientes(self):
        """
        Gerar dados de clientes usando Faker.
        """
        clientes = []
        for i in track(sequence=range(1, self.n_clientes + 1), description='Gerando dados de clientes...'):
            temp_cliente = {
                'id_cliente': i,
                'nome': fake.name(),
                'email': fake.email(),
                'data_cadastro': fake.date_between(start_date='-2y', end_date='today'),
                'cidade': fake.city()
            }
            clientes.append(temp_cliente)

        df_clientes = DataFrame(clientes)
        return df_clientes


    def gerar_dados_produtos(self):
        """
        Gerar dados de produtos usando Faker.
        """
        categorias = ['Eletrônicos', 'Livros', 'Casa', 'Vestuário', 'Esportes']
        produtos = []
        for i in track(sequence=range(1, self.n_produtos + 1), description='Gerando dados de produtos...'):
            temp_produto = {
                'id_produto': i,
                'nome_produto': f'Produto {fake.word().capitalize()}',
                'categoria': random.choice(categorias),
                'preco': round(random.uniform(10.0, 2000.0), 2)
            }
            produtos.append(temp_produto)
        df_produtos = DataFrame(produtos)
        return df_produtos

    def gerar_dados_pedidos_itens(self):
        """
        Gerar dados de pedidos e itens dos pedidos usando Faker.
        """
        pedidos = []
        for i in track(sequence=range(1, self.n_pedidos + 1), description='Gerando dados de pedidos...'):
            temp_pedido = {
                'id_pedido': i,
                'id_cliente': random.randint(1, self.n_clientes),
                'data_pedido': fake.date_between(start_date='-1y', end_date='today')
            }
            pedidos.append(temp_pedido)
        df_pedidos = DataFrame(pedidos)
        return df_pedidos

    def gerar_dados_itens(self, df_produtos):
        """
        Gerar dados de itens dos pedidos usando Faker.
        """
        itens = []
        for i in track(sequence=range(1, self.n_pedidos * 2), description='Gerando dados de itens...'): # Média de 2 itens por pedido
            id_prod = random.randint(1, self.n_produtos)
            temp_item = {
                'id_pedido': random.randint(1, self.n_pedidos),
                'id_produto': id_prod,
                'quantidade': random.randint(1, 5),
                'preco_unitario': df_produtos.loc[df_produtos['id_produto'] == id_prod, 'preco'].values[0]
            }
            itens.append(temp_item)
        df_itens = DataFrame(itens)
        return df_itens
    
    def enviar_dados_mysql(self, df_clientes, df_produtos, df_pedidos, df_itens) -> None:
        """
        Enviar dados gerados para o banco de dados MySQL.
        """
        # Enviar para o MySQL
        df_itens.to_sql('itens_pedido', con=self.engine, if_exists='replace', index=False)
        df_produtos.to_sql('produtos', con=self.engine, if_exists='replace', index=False)
        df_pedidos.to_sql('pedidos', con=self.engine, if_exists='replace', index=False)
        df_clientes.to_sql('clientes', con=self.engine, if_exists='replace', index=False)
    
        print("Banco GlobalTech E-commerce gerado com sucesso!")
        return None

if __name__ == '__main__':
    generator = GlobalTechDataGen(n_clientes=100, n_produtos=20, n_pedidos=500)
    
    df_clientes = generator.gerar_dados_clientes()
    df_produtos = generator.gerar_dados_produtos()
    df_pedidos = generator.gerar_dados_pedidos_itens()
    df_itens = generator.gerar_dados_itens(df_produtos)

    generator.enviar_dados_mysql(df_clientes, df_produtos, df_pedidos, df_itens)