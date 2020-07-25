import scrapy


def address_string(address):
    address_str = address[0]
    address_str = address_str.replace("\n", "")
    address_str = address_str.replace("\t", "")
    address_str = address_str.replace("|", "")

    return address_str


def extract_number(s):
    p = s.split("-")
    number_list = []
    number_string = "+(91)-"
    for i in range(len(p)):
        p1 = p[i].split('''"''')
        if i != 0:
            number_list.append(p1[0])

    # print(number_list[6:])
    for i in number_list[6:]:
        if i == "ji":
            number_string += "9"
        elif i == "lk":
            number_string += "8"
        elif i == "nm":
            number_string += "7"
        if i == "po":
            number_string += "6"
        elif i == "rq":
            number_string += "5"
        elif i == "ts":
            number_string += "4"
        if i == "vu":
            number_string += "3"
        elif i == "wx":
            number_string += "2"
        elif i == "yz":
            number_string += "1"
        elif i == "acb":
            number_string += "0"

    return number_string


class JdSpider(scrapy.Spider):
    name = "JustDial"
    base_url = "https://justdial.com/Delhi/House-On-Rent/nct-10192844/page-"

    handle_http_status = ['504']

    def start_requests(self):
        for page in range(2):
            next_page = self.base_url + str(page)
            try:
                yield scrapy.Request(url=next_page, callback=self.parse)

            except IndexError:
                break

    def parse(self, response):
        all_data = response.css(".colsp")

        for agent in all_data:
            name = agent.css('span.lng_cont_name::text').extract()
            rating = agent.css('span.green-box::text').extract()
            address = agent.css('.cont_sw_addr::text').extract()
            contact_info = agent.css(".mobilesv").extract()

            # print("="*50)
            # print(contact_info)

            address_str = address_string(address)

            contact_number = extract_number(str(contact_info))
            yield {
                'NAME': name[0],
                "Rating": rating[0],
                "Address": address_str,
                "Contact": contact_number
            }
            # print("="*50)
