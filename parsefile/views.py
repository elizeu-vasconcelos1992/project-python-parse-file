from .models import Store, Transaction
from .type import tipos
from django.shortcuts import render
import locale
from datetime import datetime


def cnab_file(request):
    
    if request.method == "POST" and "Upload" in request.POST:
        # Buscando arquivo com dados CNAB
        uploadedFile = request.FILES["uploadedFile"]

        # Iterando sobre cada linha do arquivo.txt
        for x in uploadedFile:
            data = str(x.decode('utf-8'))
            tipo = data[0:1]
            date = data[1:9]
            valor = data[9:19]
            cpf = data[19:30]
            cartao = data[30:42]
            hora = data[42:48]
            dono = data[48:62]
            loja = data[62:81].strip()

            # Tratamento tipo de transação
            for key, value in tipos.items():
                if key == tipo:
                    tipo = value

            # Tratamento da data
            normalize_date = datetime(int(date[0:4]), int(date[4:6]), int(date[6:8]), int(hora[0:2]), int(hora[2:4]), int(hora[4:6]))
            date = normalize_date

            # Tratamento do valor
            normalize_valor = float(valor)/100
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            valor = locale.currency(normalize_valor, grouping=True, symbol=False)

            # Verificando se a loja existe no banco de dados ou criando uma
            store, _ = Store.objects.get_or_create(name=loja, owner=dono, saldo=None)

            # Salvando transação para a loja encontrada ou criada
            Transaction.objects.create(
                tipo=tipo,
                data=date,
                valor=valor,
                cpf=cpf,
                cartao=cartao,
                store=store
            )
              
    # Buscando dados das transações
    cnab_data = Transaction.objects.all()

    # Buscando dados das lojas
    cnab_store = Store.objects.all()

    # Calculando o saldo total da loja de acordo com o tipo de transacao
    for loja in cnab_store:
            sum = 0
            for item in cnab_data:
                if loja.id == item.store.id:
                    value = float(item.valor.replace(",","").replace(".", ""))
                    value = value/100
                    if item.tipo == "Financiamento" or item.tipo == "Boleto" or item.tipo == "Aluguel":
                        sum -= value
                    else:
                        sum +=value
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
            valor = locale.currency(sum, grouping=True, symbol=False)
            Store.objects.filter(id=loja.id).update(saldo=valor)


    # Buscando dados atualizados das transacoes
    cnab_data_update = Transaction.objects.all()

    # Buscando dados atualizados das lojas
    cnab_store_update = Store.objects.all()

    # Lógica para deletar arquivos do banco de dados
    if request.method == 'POST' and 'delete' in request.POST:
        cnab_store_update.delete()

    # Retornando dados para renderizacao
    return render(request, "parsefile/upload-file.html", context = {
        "files2": cnab_store_update, "files": cnab_data_update
    })

    
  


    