import requests as r




def get_zones():
    url = "https://www.thewindpower.net/country_zones_en_27_poland.php"
    for i in range(1195, 1211):
        url = f"https://www.thewindpower.net/zones_en_27_{i}.php"
        with open("elo.txt", "a") as f:
            f.write(f"{url}\n")


def get_windfarms():
    with open("elo.txt", "r") as f:
        urls = f.read().split("\n")
        for url in urls:
            if url == "":
                return None
            result = r.get(url)
            print(result.status_code, url,  "\n")
            text = result.text
            text = text.split('<td style="width:50%;" class="entete_tableau"><b>Name</b></td>')[1]
            text = text.split('href="windfarm_en_')
            text.pop(0)
            with open("linki.txt", "a") as l:
                for element in text:
                    link = element.split('">')[0]
                    link = "https://www.thewindpower.net/" + "windfarm_en_" + link
                    l.write(f"{link}\n")
    return None



def get_farms_data():
    with open("linki.txt", "r") as f:
        urls = f.read().split("\n")
        with open("data.json", "w") as d:
                d.write("{\n")
        for url in urls:
            if url == "":
                with open("data.json", "a") as d:
                    d.write("}")
                return None
            result = r.get(url)
            text = result.text
            text = text.split("<h1>Details</h1>")[1]
            text = text.split("<h1>Localisation</h1>")[0]
            text = text.split("Total nominal power: ")
            text.pop(0)
            value = 0
            for _t in text:
                value = value + float(_t.split(" ")[0].replace(",", "."))
            print(value, url)
            
            with open("data.json", "a") as d:
                d.write(f'"{url.split("_")[-1].split(".")[0]}": {value},\n')
            
        with open("data.json", "a") as d:
                d.write("}")
    return None


get_zones()
get_windfarms()
get_farms_data()