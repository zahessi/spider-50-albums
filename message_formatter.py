

class MessageFormatter:

    def create_message_for_album(self, item):
        artistalbum = item.artist.split(" ") + item.album.split(" ")
        google_music = "https://play.google.com/music/listen?u=0#/sr/" + "+".join(artistalbum)
        data = [
            f"{item.artist} - {item.album}",
            (f"genres - {item.genres}, " if item.genres != "[]" else '') + f"year - {item.year}",
            f"[review]({item.review_url})[.]({item.picture_url}) [google music]({google_music})"
        ]
        return '\n'.join(data)
