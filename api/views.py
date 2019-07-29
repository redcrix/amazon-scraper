from django.http import HttpResponse
from django.shortcuts import render
from .forms import InputForm
from bs4 import BeautifulSoup
import urllib3
import pandas as pd


def input(request):
    if request.POST:
        inputform = InputForm(request.POST)
        if inputform.is_valid():
            url=str(request.POST.get('url'))
            n=int(request.POST.get('page_no'))

            ################################################################################

            def level1(url, soup, a):
                for i in soup.find_all('h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-2'):
                    if '/dp/' in i.find('a').attrs['href']:
                        if a > 5:
                            break
                        level2(str('https://www.amazon.in' + i.find('a').attrs['href']))
                        a += 1
                return print(url, " MU>>> Done")

            def level2(purl):
                p_http = urllib3.PoolManager()
                p_response = p_http.request('GET', purl)
                a = BeautifulSoup(p_response.data)
                with open("testing.html", "w") as file:
                    file.write(str(a))

                p_soup = BeautifulSoup(open("testing.html"), "html.parser")



                print('>>> ', purl)

                f.write('"')
                try:
                    f.write(str(p_soup.find('span', id='productTitle').text.strip().replace('"', "'")))
                except:
                    print("Item not found", end=' ')
                f.write('"')

                f.write(',')

                print('[ =', end=' ')

                f.write('"')
                try:
                    f.write(str(p_soup.find('a', id='bylineInfo').text.strip()))
                except:
                    print("Item not found", end=' ')
                f.write('"')

                f.write(',')

                print('=', end=' ')

                f.write('"')
                f.write(str(purl))
                f.write('"')

                f.write(',')

                print('=', end=' ')

                f.write('"')
                try:
                    for div in p_soup.findAll('div', {'id': 'imgTagWrapperId'}):
                        f.write(str(div.find('img')['data-a-dynamic-image'].split('"')[1]))
                except:
                    print("Item not found", end=' ')
                f.write('"')

                f.write(',')

                print('=', end=' ')

                f.write('"')
                try:
                    f.write(str(p_soup.find('span', class_='priceBlockStrikePriceString a-text-strike').text.strip()))
                except:
                    try:
                        f.write(str(p_soup.find('span', id='priceblock_ourprice').text.strip()))
                    except:
                        try:
                            f.write(str(p_soup.find('span', id='priceblock_dealprice').text.strip()))
                        except:
                            print("Item not found", end=' ')
                f.write('"')

                f.write(',')

                print('=', end=' ')

                f.write('"')
                try:
                    f.write(str(p_soup.find('span', class_='arp-rating-out-of-text a-color-base').text.strip()))
                except:
                    print("Item not found", end=' ')
                f.write('"')

                f.write(',')

                print('=', end=' ')

                f.write('"')
                try:
                    f.write(str(p_soup.find('span', id='acrCustomerReviewText').text))
                except:
                    print("Item not found", end=' ')
                f.write('"')

                f.write(',')

                print('=', end=' ')

                f.write('"')
                try:
                    for div in p_soup.findAll('a', {'id': 'askATFLink'}):
                        f.write(str(div.find('span', class_='a-size-base').text.strip()))
                except:
                    print("Item not found", end=' ')
                f.write('"')

                f.write(',')

                print('=', end=' ')

                f.write('"')
                try:
                    for div in p_soup.findAll('div', {'id': 'productDescription'}):
                        f.write(str(div.find('p').text.strip().replace('"', "'")))
                except:
                    print("Item not found", end=' ')
                f.write('"')

                f.write(',')

                print('=', end=' ')

                f.write('"')
                try:
                    for div in p_soup.findAll('div', id='feature-bullets'):
                        for i in div.findAll('span', class_='a-list-item'):
                            f.write(str(i.text.strip().replace('"', "'")))
                except:
                    print("Item not found", end=' ')
                f.write('"')

                f.write(',')

                print('=', end=' ')

                f.write('"')
                try:
                    for div in p_soup.findAll('div', class_='a-expander-content reviewText review-text-content a-expander-partial-collapse-content'):
                        for i in div.findAll('span'):
                            f.write(str(i.text.strip().replace('"', "'")))
                            f.write('***')
                except:
                    print("Item not found", end=' ')
                f.write('"')
                f.write('\n')

                print('= ]')

                return print(purl, ' PU>>> Done')

            def result():

                data = pd.read_csv('1.csv')
                scraped_json = data.to_json()

                #print(scraped_json)

                price = []
                for i in data['Product_price']:
                    try:
                        price.append(int(i.split('\xa0')[1].replace(',', '').split('.')[0]))
                    except:
                        price.append(0)

                rating = []
                for i in data['rating']:
                    try:
                        rating.append(float(i.split(' ')[0]))
                    except:
                        rating.append(float(0))
                total_review = []
                for i in data['total_review']:
                    try:
                        total_review.append(int(i.split(' ')[0].replace(',', '')))
                    except:
                        total_review.append(0)
                ans_ask = []
                for i in data['ans_ask']:
                    try:
                        ans_ask.append(int(i.split(' ')[0].replace('+', '')))
                    except:
                        ans_ask.append(0)

                score = []
                for i in range(len(data.Product_name)):
                    if rating[i] > 2.5:
                        score.append(((rating[i] * total_review[i] + ans_ask[i]) / sum(total_review)) * 100)
                    else:
                        score.append(((rating[i] * total_review[i] - ans_ask[i]) / sum(total_review)) * 100)

                data['score'] = score

                data = data.sort_values(by=['score'], ascending=False)
                sort_json = data.to_json()
                #print(sort_json)

                return sort_json


            #   CALL   #################################################################

            f = open('1.csv', 'w')
            f.write('Product_name,by_info,Product_url,Product_img,Product_price,rating,total_review,ans_ask,prod_des,feature,cust_review\n')

            next=''

            a = 1

            while n > 0:

                http = urllib3.PoolManager()
                response = http.request('GET', url)
                soup = BeautifulSoup(response.data, 'html.parser')

                for li in soup.findAll('li', {'class': 'a-last'}):
                    next = 'https://www.amazon.in' + str(li.find('a').attrs['href'].strip())

                level1(url, soup, a)

                url = next
                n -= 1
            f.close()

            data=result()

            ##############################################################################

            return render(request, 'output.html',{'data':data})
    else:
        inputForm = InputForm()
        return render(request, 'Input.html', {'inputForm': inputForm})
