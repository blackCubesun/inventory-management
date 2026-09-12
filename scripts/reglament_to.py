import pandas as pd
import os

PROCESSED = r'C:\Users\92585\Desktop\Sklad_System\data\processed'

reglament = pd.DataFrame({
    'Модель': ['НЕФАЗ 5299', 'НЕФАЗ 5299', 'НЕФАЗ 5299', 'КАМАЗ 6282', 'КАМАЗ 6282'],
    'ВидТО': ['ТО-1', 'ТО-2', 'Сезонное ТО', 'ТО-2500', 'Периодическое ТО'],
    'ПериодичностьКм': [6000, 17000, None, 2500, 30000],
    'ПериодичностьМесяцев': [None, None, 6, None, None],
    'РесурсДоКР': [450000, 450000, None, 500000, 500000]
})

print(reglament)
reglament.to_excel(os.path.join(PROCESSED, 'Регламент_ТО.xlsx'), index=False)
print('\nСохранено: Регламент_ТО.xlsx')