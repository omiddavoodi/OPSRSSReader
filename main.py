import urllib.request

class rssreader:
    def __init__(self, address):
        self.address = address
        self.raw_contents = ""
        self.result = ""
        self.title = ""
        
    def load(self):
        self.raw_contents = urllib.request.urlopen(self.address).read()

    def parse(self):
        temp = str(self.raw_contents)
        start = temp.find("<rss")
        current = start+5
        if (start == -1):
            self.result = "Error:Failed parsing the RSS"
            return
        title = ""
        if ("<title" in temp):
            if (not ("</title>" in temp)):
                self.result = "Error:Failed parsing the RSS"
                return
            else:
                titletag = temp.find("<title", current)
                titletagclosed = temp.find("</title>", current)
                title = temp[titletag+7:titletagclosed]
                current = titletagclosed
                
        desc = ""
        if ("<description" in temp):
            if (not ("</description>" in temp)):
                self.result = "Error:Failed parsing the RSS"
                return
            else:
                desctag = temp.find("<description", current)
                desctagclosed = temp.find("</description>", current)
                desc = temp[desctag+13:desctagclosed]
                current = desctagclosed

        copyr = ""
        if ("<copyright" in temp):
            if (not ("</copyright>" in temp)):
                self.result = "Error:Failed parsing the RSS"
                return
            else:
                copyrtag = temp.find("<copyright", current)
                copyrtagclosed = temp.find("</copyright>", current)
                copyr = temp[copyrtag+11:copyrtagclosed]
                current = copyrtagclosed

        copyr = copyr.replace("\\xc2\\xa9", "©")
                
        self.title = title
        self.result += "Title:" + title + "\n"
        self.result += "Description:" + desc + "\n"
        self.result += "Copyright:" + copyr + "\n"

        itempos = temp.find("<item", current)
        itemcpos = temp.find("</item>", current)

        feeds = 0
        while (itempos != -1):
            feeds += 1
            currentitem = temp[itempos:itemcpos]
            tcurrent = 0
            title = ""
            if ("<title" in currentitem):
                if (not ("</title>" in currentitem)):
                    self.result = "Error:Failed parsing the RSS"
                    return
                else:
                    titletag = currentitem.find("<title", tcurrent)
                    titletagclosed = currentitem.find("</title>", tcurrent)
                    title = currentitem[titletag+7:titletagclosed]
                    tcurrent = titletagclosed
            
            link = ""
            if ("<link" in currentitem):
                if (not ("</link>" in currentitem)):
                    self.result = "Error:Failed parsing the RSS"
                    return
                else:
                    linktag = currentitem.find("<link", tcurrent)
                    linktagclosed = currentitem.find("</link>", tcurrent)
                    link = currentitem[linktag+6:linktagclosed]
                    tcurrent = linktagclosed
                    
            desc = ""
            if ("<description" in currentitem):
                if (not ("</description>" in currentitem)):
                    self.result = "Error:Failed parsing the RSS"
                    return
                else:
                    desctag = currentitem.find("<description", tcurrent)
                    desctagclosed = currentitem.find("</description>", tcurrent)
                    desc = currentitem[desctag+13:desctagclosed]
                    tcurrent = desctagclosed

            date = ""
            if ("<pubDate" in currentitem):
                if (not ("</pubDate>" in currentitem)):
                    self.result = "Error:Failed parsing the RSS"
                    return
                else:
                    datetag = currentitem.find("<pubDate", tcurrent)
                    datetagclosed = currentitem.find("</pubDate>", tcurrent)
                    date = currentitem[datetag+9:datetagclosed]
                    tcurrent = datetagclosed

            title = title.replace("\\xe2\\x80\\x98", "'")
            title = title.replace("\\xe2\\x80\\x99", "'")
            desc = desc.replace("\\xe2\\x80\\x98", "'")
            desc = desc.replace("\\xe2\\x80\\x99", "'")
            desc = desc.replace("\\r", " ")
            self.result += "\nFeed" + str(feeds) + ":\n"
            self.result += "Date:" + date + "\n"
            self.result += "Title:" + title + "\n"
            self.result += "Description:" + desc + "\n"
            self.result += "Link:" + link + "\n"
            current = itemcpos+5
            itempos = temp.find("<item", current)
            itemcpos = temp.find("</item>", current)

q = rssreader("http://edition.presstv.ir/rss/")
q.load()
q.parse()

mfile = open(q.title+".txt", "w")
mfile.write(q.result)
mfile.close()
