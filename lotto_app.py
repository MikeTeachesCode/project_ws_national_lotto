from bs4 import BeautifulSoup
import requests, time, os
import matplotlib.pyplot as plt

class LottoApp:
    
    def __init__(self, start_year, end_year):
        self.start_year = max(start_year, 1994) # (1990, 1994)
        self.end_year = min(end_year, 2023)     # (2040, 2023)
        self.numbers_cached = []
        self.list_years = list(range(1994, 2023 + 1))
        self.top_data = None
        self.folder = "VISUAL"
    
    def scrape_data(self):
        
        if self.end_year > self.start_year:
            
            years = list(range(self.start_year, self.end_year + 1))
            for y in years:
                time.sleep(1)
                print("Web scraping year {}".format(y))
                url = "https://www.lottery.co.uk/lotto/results/archive-{}".format(y)
                html = requests.get(url).text
                soup = BeautifulSoup(html, "lxml")
                table = soup.find("table", 
                                  class_ = "table lotto mobFormat").\
                                    find_all("td", class_="noBefore")
                for i in range(1, len(table), 3):
                    balls = [int(t.text) for 
                             t in table[i].find_all("div")]
                    self.numbers_cached.append(balls)
        else:
            print("Invalid year/s chosen")

    def analyze_data(self):
        total = []
        for n in self.numbers_cached:
            total += n

        count = {i: [] for i in set(total)}
        for t in total:
            count[t].append(1)
            
        dstotal = {k: sum(count[k]) for k in count}
        
        nlist = [k for k in sorted(dstotal.items(),
               key = lambda item: item[1], reverse = True)]
        self.top_data = dict(nlist)
        
    def visualize_data(self):

        if not os.path.exists(self.folder):
            os.mkdir(self.folder) # VISUAL folder
            
        visual_path_file = self.folder + os.sep +\
        "new-lotto-{}-{}.png".format(*[self.end_year, self.start_year])
        
        freq = list(self.top_data.values())[:10]
        xlabels = list(self.top_data.keys())[:10]
        xticks = range(len(freq))
        # PLOT
        fig, ax = plt.subplots(figsize=(20, 8))
        colors = {"violet", 
                  "lightblue", 
                  "lightgreen", 
                  "pink", 
                  "red", 
                  "thistle",
                 "yellow", 
                  "orange", 
                  "silver", 
                  "purple", 
                  "brown"}
        ax.bar(x=xticks, height = freq,
              color = colors)
        ax.set_facecolor("darkcyan")
        ax.set_xticks(xticks, xlabels)
        ax.bar_label(ax.containers[0], label_type="center",fontsize=20)
        fig.suptitle(f"""{self.start_year}-{self.end_year} 
        Winning Numbers""", fontsize=28)
        ax.margins(y=0.2)
        plt.savefig(visual_path_file, bbox_inches='tight')
        plt.show()

if __name__ == "__main__":
    lotto = LottoApp(2020, 2023) # Instance of class
    lotto.scrape_data()
    lotto.analyze_data()
    lotto.visualize_data()