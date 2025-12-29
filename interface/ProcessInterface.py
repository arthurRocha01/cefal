import pandas as pd

class ProcessInterface:
    def __init__(self):
        pass

    def _sanitize_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Sanitiza os dados do DataFrame, preenchendo valores nulos e removendo espaços em branco."""
        data = data.fillna('')

        cols_strings = data.select_dtypes(include=['object']).columns
        for col in cols_strings:
            data[col] = data[col].str.strip()
        
        return data

    def read_csv(self, file_path):
        """Lê um arquivo CSV e retorna os dados como uma lista de dicionários."""
        try:
            df = pd.read_csv(file_path, dtype=str, encoding='utf-8-sig')
            df = self._sanitize_data(df)
            return df.to_dict('records')
        except Exception as e:
            raise Exception(f'Erro ao ler o arquivo CSV: {str(e)}')

    def read_xlsx(self, file_path):
        """Lê um arquivo XLSX e retorna os dados como uma lista de dicionários."""
        pass