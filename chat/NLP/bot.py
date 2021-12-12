import re
import random
class Bot:
    def checkForGreeting(self, text, intent_dict):
        greetings = intent_dict
        for greet in greetings:
            if greet.lower() == text:
                return "greetings"
    def checkForFarewell(self, text, intent_dict):
        farewells = intent_dict
        for farewell in farewells:
            if farewell.lower() == text:
                return "farewell"
    def checkForImageSelection(self, text, image_objects):
        for i, objects in enumerate(image_objects):
            num = len(objects)
            count = 0
            for object in objects:
                for word in text:
                    if word == object:
                        count += 1
            if count == num:
                return i, "gameSelection"
        return None, None
        pass
    def processText(self, text, images, selected):
        img_id = []
        img = []
        selected_id = []
        for image in selected:
            selected_id.append(image["imageId"])

        for image in images:
            if image["imageId"] not in selected_id:
                cat_name = image["imagePath"].split('\\')[2].split('_')
                img_id.append(image["imageId"])
                img.append(cat_name)
        
        intent_dict = {
            "greetings": ["hi", "hello", "hey", "helloo", "hellooo", "g morining", "gmorning", "good morning",
                          "morning", "good day", "good afternoon", "good evening", "greetings", "greeting",
                          "good to see you", "its good seeing you", "how are you", "how're you", "how are you doing",
                          "how ya doin'", "how ya doin", "how is everything", "how is everything going",
                          "how's everything going", "how is you", "how's you", "how are things", "how're things",
                          "how is it going", "how's it going", "how's it goin'", "how's it goin",
                          "how is life been treating you", "how's life been treating you", "how have you been",
                          "how've you been", "what is up", "what's up", "what is cracking", "what's cracking",
                          "what is good", "what's good", "what is happening", "what's happening", "what is new",
                          "what's new", "what is neww", "g’day", "howdy"],
            "gameSelection": img,
            "farewell": ["goodbye", "bye", "bye-bye", "good night", "quit", "stop", "end", "bbye"]
        }
        replies = {
            "greetings": ["Hi, I am a bot. Looking forward to our conversation.",
                          "Hello, this is Mr.Bot. Nice to meet you.", "Hi, let's have a good game. Good luck."],
            "gameSelection": ["I have the same contents in one image. I think this is common."],
            "farewell": ["Goodbye, have a nice day.",
                         "Bye, it was a good conversation.", "See you, it was great learning experience for me."],
            "unknown": ["Sorry, I didn't understand you. If this is about a image, I don't think I have the same one.",
                        "I don't have the same image.",
                        "I could not find any relevant match for the given description."]
        }
        text = text.lower()
        index = None
        intent = self.checkForGreeting(text, intent_dict["greetings"])
        if not intent:
            intent = self.checkForFarewell(text, intent_dict["farewell"])
        if not intent:
            index, intent = self.checkForImageSelection(re.findall(r"[\w']+|[.,!?;]", text), intent_dict["gameSelection"])
        if not intent:
            intent = 'unknown'
        reply = random.choice(replies[intent])
        if index != None:
            return img_id[index], reply
        return None, reply
