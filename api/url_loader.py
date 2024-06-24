from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.image import UnstructuredImageLoader


def fetch_detail_from_youtube(video_url:str):
    loader = YoutubeLoader.from_youtube_url(
        video_url, add_video_info=False
    )
    data=loader.load()
    print(data)
    return data

def fetch_details_from_webpage(urls):
    ls_urls=[]
    ls_urls.append(urls)
    loader = UnstructuredURLLoader(ls_urls)
    data = loader.load()
    print(data)
    return data

# def fetch_details_from_images():
#     loader = UnstructuredImageLoader("assets/image_check.png")
#     data = loader.load()
#     print(data[0])

# fetch_details_from_images()
# fetch_details_from_webpage("https://www.twilio.com/en-us/blog/build-secure-twilio-webhook-python-fastapi")