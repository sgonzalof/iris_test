import re
import webbrowser
import requests
from bs4 import BeautifulSoup
from ...domain.ports.browser_port import BrowserPort
from ...domain.value_objects.search_result import SearchResult
from ...domain.value_objects.music_track import MusicTrack
from ...domain.value_objects.video import Video

class BrowserAdapter(BrowserPort):


    def search_youtube(self, query: str) -> Video:
        try:

            query_url = query.replace(" ", "+")  # Replace spaces with plus signs
            url = f"https://www.youtube.com/results?search_query={query_url}"

            req = requests.get(url)
            if req.status_code != 200:
                raise RuntimeError(f"Failed to fetch YouTube search results: {req.status_code}")
            elif "No results found" in req.text:
                raise RuntimeError("No results found for the given query.")
            
            elif req.ok:
                match = re.search(r'videoId":"(.+?)"', req.text)
                if match:
                    video_id = match.group(1)

                    video = Video.create(
                        video_id=video_id,
                        title=query
                    )

                    url_video = f"https://www.youtube.com/watch?v={video_id}"
                    print(f"Video found: {url_video}")
                    return video
            else:
                return False
            
        except requests.RequestException as e:
            raise RuntimeError(f"Error fetching YouTube results: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error processing YouTube search: {str(e)}")
        

    def search_google(self, query: str) -> SearchResult:
        """Search in Google and return the gemini description if available"""
        try:
            # Headers to avoid being blocked
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            query_url = query.replace(" ", "+")
            url = f"https://www.google.com/search?q={query_url}"

            response = requests.get(url, headers=headers)
            response.raise_for_status()
            

            # Parse HTML with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find Gemini content (div with class WaaZC)
            gemini_divs = soup.find_all('div', class_='WaaZC')
            description = ""
            
            if gemini_divs:
                # Extract and combine text from all Gemini divs
                for div in gemini_divs:
                    # Get all text content, removing HTML tags
                    text = div.get_text(strip=True, separator=' ')
                    if text:
                        description += text + " "
            
            # If no Gemini content found, try regular search result
            if not description:
                regular_desc = soup.find('div', class_='VwiC3b')
                description = regular_desc.get_text() if regular_desc else "No description available"
            
            # Get title from first h3 element
            title_elem = soup.find('h3')
            title = title_elem.get_text() if title_elem else query

            return SearchResult(
                title=title,
                description=description.strip(),
                url=url
            )

        except requests.RequestException as e:
            raise RuntimeError(f"Error fetching Google results: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Error processing Google search: {str(e)}")
        

    def search_amazon_music(self, query: str) -> MusicTrack:
        """Search track in Amazon Music"""
        try:
            # Por ahora, simplemente redirigir a la búsqueda en Amazon Music
            query_url = query.replace(" ", "+")
            url = f"https://music.amazon.com/search/{query_url}"
            
            return MusicTrack(
                title=query,
                artist="Unknown",  # No podemos obtener estos datos sin API
                url=url
            )
        except Exception as e:
            raise RuntimeError(f"Error searching Amazon Music: {str(e)}")

    def open_url(self, url: str) -> None:
        """Open URL in default browser"""
        webbrowser.open(url)




















        
    # def search_google(self, query: str) -> SearchResult:

        
    #     try:
    #         self._driver.get(f"https://www.google.com/search?q={query}")

            
            
    #         # Wait for search results
    #         wait = WebDriverWait(self._driver, 10)
    #         first_result = wait.until(
    #             EC.presence_of_element_located((By.CSS_SELECTOR, "div.g"))
    #         )
            
    #         title = first_result.find_element(By.CSS_SELECTOR, "h3").text
    #         description = first_result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text
    #         url = first_result.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            
    #         return SearchResult(title=title, description=description, url=url)
            
    #     except Exception as e:
    #         raise RuntimeError(f"Error searching Google: {str(e)}")
        





















        
    
    # def search_youtube(self, query: str) -> Video:
    #     try:
    #         self._driver.get(f"https://www.youtube.com/results?search_query={query}")
            
    #         wait = WebDriverWait(self._driver, 10)
    #         first_video = wait.until(
    #             EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-video-renderer"))
    #         )
            
    #         video_id = first_video.get_attribute("data-video-id")
    #         title = first_video.find_element(By.CSS_SELECTOR, "#title-wrapper").text
            
    #         return Video.create(video_id=video_id, title=title)
            
    #     except Exception as e:
    #         raise RuntimeError(f"Error searching YouTube: {str(e)}")
    
    # def search_amazon_music(self, query: str) -> MusicTrack:
    #     try:
    #         self._driver.get(f"https://music.amazon.com/search/{query}")
            
    #         wait = WebDriverWait(self._driver, 10)
    #         first_track = wait.until(
    #             EC.presence_of_element_located((By.CSS_SELECTOR, ".music-track"))
    #         )
            
    #         title = first_track.find_element(By.CSS_SELECTOR, ".track-title").text
    #         artist = first_track.find_element(By.CSS_SELECTOR, ".track-artist").text
    #         url = first_track.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            
    #         return MusicTrack(title=title, artist=artist, url=url)
            
    #     except Exception as e:
    #         raise RuntimeError(f"Error searching Amazon Music: {str(e)}")
    
    # def open_url(self, url: str) -> None:
    #     self._driver.get(url)