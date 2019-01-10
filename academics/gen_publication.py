from habanero import Crossref



with open('inventors_w_aliases.csv',"r") as csvfile:
    csv_inventors = csv.reader(csvfile, delimiter=',')
    inventors_names_w_aliases  = list(csv_inventors)



def get_man_
cr = Crossref(mailto = "jedr.ka@gmail.com")
x = cr.works(query_author = "")

x['message']
x['message']['total-results']
x['message']['items']


