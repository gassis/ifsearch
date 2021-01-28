import re, requests, urllib, PyPDF4, pytesseract, base64, tempfile, time, socket, progressbar
from urllib.error import URLError
from lxml import html
from io import BytesIO
from PIL import Image
from pdf2image import convert_from_bytes
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, connections, Document, Text

ELASTICSEARCH_INDEX = 'docsearch'


class Page(Document):
    url = Text()
    year = int()
    month = Text()
    page = int()
    base64 = Text()

    class Index:
        name = ELASTICSEARCH_INDEX

    def save(self, **kwargs):
        return super().save(**kwargs)


def monitor_index():
    client = Elasticsearch('elasticsearch:9200')
    s = Search(using=client, index="docsearch")
    s = s.query("match_all")
    results = {}
    r = s.scan()
    for hit in r:
        page = hit.page + 1
        if hit.year not in results:
            results[hit.year] = {}
        if hit.month not in results[hit.year]:
            results[hit.year][hit.month] = []
        if hit.url not in results[hit.year][hit.month]:
            results[hit.year][hit.month].append(hit.url)
    items = results.items()
    sorted_items = sorted(items, reverse=True)
    client.close()
    return sorted_items


def gt_month(a, b):
    meses = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro',
             'novembro', 'dezembro']
    idx_a = idx_b = 0
    for idx, val in enumerate(meses, 1):
        if val == a.lower():
            idx_a = idx
        if val == b.lower():
            idx_b = idx
    print("->", idx_a, idx_b)
    if idx_a > idx_b:
        return True
    else:
        return False


def bulletin(ifgpage):
    page = requests.get(ifgpage + '/boletim-de-servico')
    tree = html.fromstring(page.content)
    pages = tree.xpath('//div[@class="article-index"]//a[@class="toclink"]/@href')
    result = []
    for pageitem in pages:
        #print("BOLETIM ==>" + pageitem)
        bulletindata = requests.get(ifgpage + pageitem)
        btree = html.fromstring(bulletindata.content)
        bpages = btree.xpath('//p/strong/text() | //p/b/text()')
        year = re.search(r'\d{4}$', bpages[0]).group()
        #print("Ano = " + year)
        listmonth = []
        portarias = []
        for i in range(1, len(bpages)):
            bfiles = btree.xpath('//p/strong[contains(text(), "' + bpages[
                i] + '")]/following::a[@href != "http://www.ifg.edu.br/" and @rel="alternate"]/@href | //p/b[contains(text(), "' +
                                 bpages[
                                     i] + '")]/following::a[@href != "http://www.ifg.edu.br/" and @rel="alternate"]/@href')
            listfiles = []
            for item in bfiles:
                listfiles.append(item)
            listmonth.append(set(listfiles))
            if i == len(bpages) - 1:
                portarias.append(listmonth[len(listmonth) - 1])
                for k in range(len(listmonth) - 1, 0, -1):
                    portarias.append(listmonth[k - 1] - listmonth[k])
        j = i
        for portaria in portarias:
            result.append((year, bpages[j], portaria))
            j = j - 1
    return result


def doccrawler(portarias):
    check = []
    print("#############################################################################")
    print("               PROCESSING AND INGESTING DATA IN ELASTICSEARCH                ")
    print("                   This may take a few hours to complete                     ")
    print("#############################################################################")
    for year, month, portaria in portarias:
        print("\n==> Ano: {}\tMes: {}".format(year, month))
        check.append(portarias[0])
        try:
            for itemportaria in portaria:
                url = list(urllib.parse.urlsplit(itemportaria))
                url[2] = urllib.parse.unquote(url[2], encoding='utf-8')
                url[2] = urllib.parse.quote(url[2], safe='/', encoding='utf-8')
                url = urllib.parse.urlunsplit(url)
                file = urllib.request.urlopen(url).read()
                file = BytesIO(file)
                cont = 0
                try:
                    read_pdf = PyPDF4.PdfFileReader(file, strict=False)
                    # get the read object's meta info
                    pdf_meta = read_pdf.getDocumentInfo()
                    # get the page numbers
                    num_pages = read_pdf.getNumPages()
                    for page in range(num_pages):
                        data = read_pdf.getPage(page)
                        # extract the page's text
                        page_text = data.extractText()
                        if len(page_text) == 0:
                            cont = cont + 1
                        if cont >= 5:
                            raise Exception()
                    # create a dictionary object for page data
                    meta = {}
                    for key, value in pdf_meta.items():
                        meta[key] = value
                    # iterate the page numbers
                    #print("\n==>", url, year, month)
                    bar = progressbar.ProgressBar(max_value=num_pages)
                    for page in range(num_pages):
                        data = read_pdf.getPage(page)
                        page_text = data.extractText()
                        bytes_string = bytes(page_text, 'utf-8')
                        encoded_pdf = base64.b64encode(bytes_string)
                        encoded_pdf = str(encoded_pdf, 'utf-8')
                        document = Page(
                            url=url,
                            year=year,
                            month=month,
                            page=page,
                            base64=encoded_pdf,
                        )
                        document.save(pipeline='docsearch-extract-pdf')
                        time.sleep(0.1)
                        bar.update(page+1)
                except:
                    # print(" ==> Warning: Proceeding with Alternative Data Extraction (IMAGE TRANSFORMATION) !")
                    f = file.getvalue()
                    with tempfile.TemporaryDirectory() as path:
                        images = convert_from_bytes(f, 300, output_folder=path)
                    #print("\n==>", url, year, month)
                    bar = progressbar.ProgressBar(max_value=num_pages)
                    for page, image in enumerate(images):
                        buffer = BytesIO()
                        image.save(buffer, "JPEG")
                        # Recognize the text as string in image using pytesserct
                        text = str((pytesseract.image_to_string(Image.open(buffer))))
                        page_text = text.replace('-\n', '')
                        # put the text data into the dict
                        bytes_string = bytes(page_text, 'utf-8')
                        encoded_pdf = base64.b64encode(bytes_string)
                        encoded_pdf = str(encoded_pdf, 'utf-8')
                        document = Page(
                            url=url,
                            year=year,
                            month=month,
                            page=page,
                            base64=encoded_pdf,
                        )
                        document.save(pipeline='docsearch-extract-pdf')
                        buffer.close()
                        time.sleep(0.1)
                        bar.update(page+1)
                file.close()
        except (ConnectionError, URLError, socket.gaierror):
            rest = set(portarias) - set(check)
            print("***************************** SISTEMA TEMPORARIAMENTE INDISPONIVEL ***************************** ")
            print("\t\t\t\t Tempo de Espera = 60 minutos ")
            time.sleep(3600)
            doccrawler(rest)


def monitor():
    print("Iniciando o processo de Indexacao (Elasticsearch)...")
    try:
        tempdir = '/home/gustavo/PycharmProjects/docsearch/temp/'
        ifgpage = "https://www.ifg.edu.br"
        connections.create_connection(hosts=['elasticsearch:9200'], timeout=20)
        es_data = monitor_index()
        docs = bulletin(ifgpage)
        insert = []
        for year, month, portarias in docs:
            p_select = set()
            for item in portarias:
                url = list(urllib.parse.urlsplit(ifgpage + item))
                url[2] = urllib.parse.unquote(url[2], encoding='utf-8')
                url[2] = urllib.parse.quote(url[2], safe='/', encoding='utf-8')
                page = urllib.parse.urlunsplit(url)
                p_select.add(page)
            if es_data:
                if int(es_data[0][0]) == int(year):
                    for key, value in es_data[0][1].items():
                        if key == month:
                            if p_select - set(value):
                                insert.append((year, month, p_select - set(value)))
                            break
                        elif not gt_month(key, month):
                            insert.append((year, month, p_select))
                            break
                elif int(es_data[0][0]) < int(year):
                    insert.append((year, month, p_select))
            else:
                insert.append((year, month, p_select))
        if insert:
            doccrawler(insert)
    except requests.exceptions.ConnectionError as e:
        print("## monitor ERROR 1: ##", e)
        time.sleep(5)
        monitor()
    except socket.error as e:
        print("## monitor ERROR 2: ##", e)
        time.sleep(5)
        monitor()
        
monitor()
