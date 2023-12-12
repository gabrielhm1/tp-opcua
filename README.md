## Prerequisitos
- Docker
- Docker Compose

## Como Executar
O projeto foi desenvolvido utilizando Docker para facilitar a execução de todos os componentes. O único componente externo é o servidor OPC que está sendo simulado através do software PROSYS Server
1. Inicie o Prosys Server
1. Faça o build das aplicações na raiz desse projeto, executando o comando: `docker build -t python-apps`
2. Por fim execute os containers com o comando: `docker-compose up`
3. Com isso todos os componentes necessários estarão sendo executados.

## Configuração do Dashboard
O Dashboard utiliza o InfluxDB para coletar e armazenar os dados do Servidor OPC. Para visualização é utilizado o Grafana.
### InfluxDB
1. Acesse o InfluxDB pela url `localhost:8086`
2. Após cadastrar seu usuário clique em Sources e procure por **opcua**
3. Clique em **Use this plugin** e cole todas as informações disponível na seção `inputs.opcua` do arquivo `dashboard/telegraf/telegraf.conf` no campo de configuração que será disponibilizado.
4. Clique em **Save And Test**
5. Será disponibilizado um token, copie e cole na varíavel `token` dentro do arquivo `dashboard/telegraf/telegraf.conf`

### Grafana

1. Acesse o Grafana pela URL `localhost:3000` usando as credenciais padrão (admin/admin).
2. Na página inicial, clique em **Add your first data source**.
3. Escolha **InfluxDB** na lista de data sources.
4. Em **HTTP**, insira `http://influxdb:8086` como URL do servidor InfluxDB.
5. Preencha os campos **Database**, **User**, e **Password** com as informações corretas de acordo com o que foi configurado no InfluxDB.
6. Clique em **Save & Test** para verificar se a conexão com o InfluxDB foi estabelecida com sucesso.

### Importando o Dashboard

1. No painel lateral esquerdo, clique no ícone **+** e selecione **Import**.
2. No campo **Grafana.com Dashboard**, insira o ID do dashboard que está disponível no arquivo `dashboard/dashboard.json`.
3. Escolha o data source recém-configurado no campo **InfluxDB**.
4. Clique em **Load** para visualizar o dashboard e, em seguida, em **Import** para adicioná-lo ao seu Grafana.

## TCP CLient
O TCP Client (Painel do operador) está sendo executado em um container, para acessar siga os passos abaixo:
1. Execute o comando `docker ps --filter "name=tcp_client"`
2. Copie o **Container ID** e execute o comando `docker exec -it <container-id> bash`
3. Por fim execute o comando para iniciar a aplicação, `python tcp_client.py`
