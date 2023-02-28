# Análise de Churn em uma Empresa de Telefonia e Internet

Este é um estudo de caso sobre o problema de churn em uma empresa de telefonia e internet. O churn é a perda de clientes que cancelam seus serviços, e é um problema crítico que pode afetar negativamente a receita e a imagem da marca da empresa.

A empresa oferece serviços de telefonia e internet, incluindo:
> Planos de telefone fixo, de dados móveis e de banda larga.  
> Pacotes de TV a cabo, de Streaming de Filmes e de
> Serviços de Backup Online, Segurança online e Seguro de Dispositivo 

O objetivo é identificar os principais fatores que influenciam a taxa de churn e propor soluções para reduzir essa taxa e reter os clientes.

Os dados foram coletados a partir de várias fontes, incluindo registros de clientes, informações de faturamento e logs de chamadas de suporte. O conjunto de dados contém informações demográficas dos clientes, histórico de pagamentos e uso de serviços.

A análise exploratória dos dados será realizada para identificar padrões e tendências nos dados, bem como relacionamentos entre as variáveis. Em seguida, serão aplicadas técnicas de modelagem preditiva para prever a taxa de churn e identificar os principais fatores que contribuem para essa taxa. 

Também serão propostas soluções para reduzir a taxa de churn, como melhorar a qualidade do serviço, ajustar preços, oferecer promoções e incentivos de fidelização, e melhorar o atendimento ao cliente. O resultado esperado é fornecer insights valiosos sobre o problema de churn em uma empresa de telefonia e internet e fornecer recomendações práticas para reduzir essa taxa e reter os clientes.

### Análise Exploratória dos Dados

Do Banco de dados:  
<img src="../figs/table_plotly.png" alt="Variáveis do Banco de dados" title="Variáveis do Banco de dados" width="500" height="500" />

O banco de dados apresenta variáveis de assinatura ou não de serviços, bem como do tempo que o cliente está na empresa e o valor de seus gastos. Há ainda informações demográficas e de pagamentos.
Segundo o Dataset a empresa pedreu nesse período um total de R$ 139130.85 em assinaturas que deixaram a empresa.

Aplicando uma análise de correlações lineares preliminar, o seguinte mapa de calor foi construido:
<img src="../figs/heatmap.png" alt="Variáveis do Banco de dados" title="Variáveis do Banco de dados" width="800" height="800" />

A princípio poucas variáveis apresentam grande impacto no Churn de clientes. Porém destaca-se a correlação negativa entre o MesesDeContrato e o Churn, indicando que clientes que estão a bastante tempo na empresa tem menor propensão de sair, e a correlação entre a ContaMensal e o Churn, indicando que quanto maior o valor da conta maior é a propensão do cliente deixar a empresa.  
Outra correlação interessantes é a da Conta Mensal, com a assinatura de diversos serviços, indicando que estes têm um impacto positivo no valor dessa variável. Mas para avaliar melhor esses impactos será feito primeiramente um balanceamento dos dados.

### Balanceamento dos dados
É comum em um problema dessa natureza que os dados disponpiveis sejam desbalanceados, já que poucos clientes costumam deixar a empresa.
<img src="../figs/barplot_desbal.png" alt="Variáveis do Banco de dados" title="Variáveis do Banco de dados" width="600" height="600" />
O balanceamento foi feito, para a aplicação de modelos de Machine Learning, por "Random Sampling", resultando na seguinte condição:
<img src="../figs/barplot_bal.png" alt="Variáveis do Banco de dados" title="Variáveis do Banco de dados" width="600" height="600" />
Além das variáveis categóricas de assinarturas de serviços e metodos de pagamento, o numero de meses de contrato do cliente e o valor de sua conta são variáveis importantes.
<img src="../figs/kdplot_meses_valorconta.png" alt="Variáveis do Banco de dados" title="Variáveis do Banco de dados" width="800" height="800" />
Observando o gráfico de dempo de contrato, percebe-se que a partir de 20 meses, aproximadamente, os clientes mudam a tendência de sair e começam a se fidelizar. 
Já para a distribuição do montante da conta mensal dos clientes, observa-se que clientes que tem um valor baixo na conta tendem a ficar, enquanto que poucos clientes que pagam um valor elevado acabam deixando a empresa.

### Modelos de Aprendizado de Máquina.
Para idenficar se um novo cliente tem tendencia de deixar a empresa, serão usados modelos de aprendizado de máquina.
Primeiramente doram testados os seguintes modelos e hiperparametros:
>KNN com 8 neighbors  
>Árvore de Decisão com profundidade máxima de 5  
>Regressão logistica com regularização *elasticnet* com proporção de L1 de 0,5 e regularização de 0.9.  
>Random Forest com profundidade máxima de 5 e 60 estimadores  
>GradientBoostg com 30 estimadores  

O melhor modelo, foi avaliado via treino e teste, com 30% para teste.  
As métricas utilizadas foram a Área abaixo da curva ROC e F1 para os dados de Treino e de Teste.  
O Gradient Boosting foi o melhor modelo com roc_auc de 0.7783 e F1 de 0.6437 para os dados de teste e roc_auc de 0.7757 e F1 de 0.6138 para os dados treino.    
Para avaliar melhor os hiperparâmetros do modelo foi realizado um GridSearch varrendo a profundidade dos estimadores e número de estimadores. O Melhor modelo foi o de profundidade 2 com 50 estimadores com score F1 de 0.63 para o treino e 0.65 para o teste.

### Importância de Variáveis com SHAP
Para entender um pouco como o modelo interpreta os dados, utiliza-se a bibluiteca SHAP. Ela retora a importância de cada variável para a previsão do modelo. Abaixo está o gráfico com a importancia da decisão do modelo para cada variável em cada entrada do dataset.
<img src="../figs/vai_imp_gradient.png" alt="Variáveis do Banco de dados" title="Variáveis do Banco de dados" width="800" height="800" />
Observa-se de cima para baixo das variáveis com maior impacto no modelo para as com menor impacto no mesmo e ao lado há uma barra de valores das variaveis, de seu máximo ao mínimo.  
O tipo de contrato ser mensal teve um grande peso para separar os clientes, o que indica que ter contrato mensal leva os clientes a saíram da empresa, enquanto que não ter o contrato mensal pode fidelizar o cliente.  
Como o esperado na análise gráfica, o numero de meses de contrato é um indicativo de fidelidade do cliente, para o modelo o impacto na decisão foi grande, indicando maiores valores de meses de contrato levam o modelo a prever que o cliente não irá sair.  
Para o modelo, os clientes que possuem assinatura de fibra óptica, que não assinam serviços de segurança online, que pagam com cheque digital e que não assinam o suporte técnico, são mais propensos a deixar a empresa.  
Já para o valor ca donta mensal, para o modelo, quanto maior o valor da mesma, maior a propensão do cliente deixar a empresa.
Em contraste com o tipo de contrato mensal, para o modelo, clientes com contrato de dois anos, têm menor propensão de deixar a empresa.

