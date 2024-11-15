import FormatFactory
import json
import re

class TextFormatFactory(FormatFactory.FormatFactory):

    __phrasesVideo:list = ["",""]
    __phrasesHeader:list = ["",""]
    #TODO

    def __init__(self) -> None:
        super().__init__()
        pass
    
    def prepareDataForTheFormat(self,itemsData: dict, includeParams: list) -> str:
        videosData:str = ""
        for info in itemsData["items"]:
            #Title and Position, Mandatory
            try:
                videosData += (str)(info["snippet"]["position"]) + ". " + info["snippet"]["title"] + " "
            except:
                videosData += "Video Unavailable "
            if includeParams[2] == True: #Author
                try:
                    videosData += "- "+info["snippet"]["videoOwnerChannelTitle"] + ", "
                except:
                    try:
                        videosData += "- "+info["snippet"]["videoOwnerChannelId"] + ", "
                    except:
                        videosData += " ,"
            if includeParams[3] == True: #Video address
                try:
                    videosData += "https://www.youtube.com/watch?v=" + info["contentDetails"]["videoId"] + " , "                
                except:
                    videosData += "Video address unavailable, "                             
            if includeParams[4] == True: #Author address
                try:
                    videosData += "Authors channel: "+"https://www.youtube.com/channel/"+info["snippet"]["videoOwnerChannelId"] + " , "              
                except:
                    videosData += "Author channel unavailable, "  
            if includeParams[5] == True: #Description
                description = ""
                try:
                    description = info["snippet"]["description"]
                    description = ' '.join(description.splitlines())
                except:
                    description = "Unavailable"
                videosData += "Description: " + description + ". "                
            if includeParams[6] == True: #Upload date
                try:
                    videosData += "Upload date: "+info["contentDetails"]["videoPublishedAt"] + ", "              
                except: 
                    videosData += "Upload date: --.--.--, "          
            if includeParams[7] == True: #Thumbnail url
                try:
                    videosData += "Thumbnail: " + info["snippet"]["thumbnails"]["maxres"]["url"] + " "              
                except:
                    try:
                        videosData += "Thumbnail: " + info["snippet"]["thumbnails"]["default"]["url"] + " "               
                    except:
                        videosData += "Thumbnail unavailable "
            videosData += "\n"                
        return videosData

    def prepareDataHeader(self,playlistInfo,includeParams: list) -> str:
        header:str = ""
        readableInfo:str = ""
        paramsData:str = ""
        for p in includeParams:
            paramsData += "1" if p else "0"
        for info in playlistInfo["items"]:
            header = "{\n\"playlistId\":\""+info["id"]+"\",\n\"channelId\":\""+info["snippet"]["channelId"]+"\",\n\"includedData\":\""+paramsData+"\"\n}\n"
            readableInfo = "Playlist Title: " + info["snippet"]["title"] + ", Created at: " + info["snippet"]["publishedAt"]
            readableInfo +=  "\nDescription: "+info["snippet"]["description"] + "\nVisible videos: " 
            readableInfo += (str)(info["contentDetails"]["itemCount"]) + "\nPlaylist owner: "+info["snippet"]["channelTitle"] + "\n\n"
        return header+readableInfo
    
    def readHeader(self, data:str)-> dir:
        infoDir:dir
        match = re.match("{[^()]+}", data)
        if match:
            infoDir = json.loads(data[match.start():(match.end()+1)])
        match = re.match(re.compile("Playlist Title: [^()]+,"), data)
        infoDir["playlistTitle"] = data[match.start():(match.end())]
        match = re.match(re.compile("Created at: [^\\n]+[\\n\\t\\r]{\\1}"), data)
        infoDir["createdAt"] = data[match.start():(match.end())]
        match = re.match(re.compile("Description: [^\\n]+[\\n\\t\\r]{\\1}"), data)
        infoDir["description"] = data[match.start():(match.end())]
        match = re.match(re.compile("Visible videos: [^\n]+[\n\t\r]{\\1}"), data)
        infoDir["visibleVideos"] = data[match.start():(match.end())]                        
        match = re.match(re.compile("Playlist owner: [^\\n]+[\\n\\t\\r]{\\1}"), data)
        infoDir["playlistOwner"] = data[match.start():(match.end())] 
        return infoDir
    
    def readFile(self):
        return super().readFile()
    pass