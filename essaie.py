# from chatterbot import ChatBot, Trainer, corpus
# import random
#
# # 3. Initialize an instance of the chatbot:
#
#
# chatbot = ChatBot('SuperMarketBot')
#
#
# # 4. Add a trainer to teach the chatbot phrases and responses related to supermarket management:
#
#
# trainer = Trainer(chatbot)
# trainer.add_training("What items are available in the store?", "Here is a list of available items: apples")
# # Add more training examples here, focusing on supermarket-related phrases and responses
# trainer.train()
#
#
# # 5. Define functions to handle specific queries related to inventory management or order fulfillment:
#
#
# def get_available_items(chatbot):
#     items = ['apples', 'bananas', 'bread', 'milk']  # Replace with actual available items
#     return f"Here is a list of available items: {', '.join(items)}"
#
# def process_item_request(chatbot, item):
#     if item in inventory:
#         response = f"We have {item}. Please come to the store to pick it up."
#     else:
#         response = "Sorry, we don't currently have that item in stock."
#     return response
#
# # 6. Integrate these functions into the chatbot's conversational flow or decision tree:
#
#
# def handle_item_request(chatbot, query):
#     # Use NLP techniques to extract the requested item from the user query
#     item = extract_item_from_query(query)
#
#     if item is not None:
#         response = process_item_request(chatbot, item)
#     else:
#         response = "I'm sorry, I didn't understand which item you were asking about."
#
#     return response
#
# def extract_item_from_query(query):
#     # Add code to extract the requested item from the user query using NLP techniques
#     pass
#
# # Add the new functions as responses for specific queries:
# chatbot.set_response("What items are available in the store?", get_available_items)
# chatbot.set_response(r"(I|me|my)\ want\ (.+)", handle_item_request)
#
# # 7. Finally, create a main function to start the chatbot and process user input:
#
# def main():
#     while True:
#         query = input("User: ")
#         response = chatbot.get_response(query)
#         print("Bot:", response)
#
# if __name__ == "__main__":
#     main()


import ollama


inventaire = {
    "Aliments": [
        {"Nom": "Pain", "Sous-Catégorie": ["Blond", "Brun", "Integral"],
         "Quantité": [50, 30, 20], "Prix": [0.50, 0.60, 0.70],
         "Date de fabrication": ["2022-01-01", "2022-02-01", "2022-03-01"],
         "Date d'expiration": ["2024-01-01", "2024-02-01", "2024-03-01"]},
        {"Nom": "Fromage", "Sous-Catégorie": ["Mozzarella", "Cheddar", "Gouda"],
         "Quantité": [30, 0, 15], "Prix": [2.00, 3.50, 4.00],
         "Date de fabrication": ["2022-01-15", "2022-02-15", "2022-03-15"],
         "Date d'expiration": ["2024-07-15", "2024-08-15", "2024-09-15"]},
    ],
    "Beverages": [
        {"Nom": "Eau", "Sous-Catégorie": [],
         "Quantité": [100], "Prix": [0.50],
         "Date de fabrication": ["2022-01-01"],
         "Date d'expiration": ["2024-01-01"]},
        {"Nom": "Jus de fruit en bouteille", "Sous-Catégorie": [],
         "Quantité": [15], "Prix": [3.00],
         "Date de fabrication": ["2022-02-01"],
         "Date d'expiration": ["2024-02-01"]},
    ],
    "Hygiène": [
        {"Nom": "Produits de toilette", "Sous-Catégorie": ["Savon"],
         "Quantité": [20], "Prix": [5.00],
         "Date de fabrication": ["2022-03-01"],
         "Date d'expiration": ["2024-03-01"]},
        {"Nom": "Lessive pour les vêtements", "Sous-Catégorie": [],
         "Quantité": [15], "Prix": [2.50],
         "Date de fabrication": ["2022-04-01"],
         "Date d'expiration": ["2024-04-01"]},
    ],
    "Électronique": [
        {"Nom": "Television", "Sous-Catégorie": ["LG", "Sony", "Samsung", "Hisense"],
         "Quantité": [10, 3, 5, 8], "Prix": [1000.00, 836, 790, 600],
         "Etat": ["4k 52 inch", "UHD 48 inch", "4K 48 inch", "8K 42 inch", "UHD 3D 52 inch"],
         }
    ]
}
while True:
    user = input("User: ")
    if user.lower() != "stop":
        b = {'role': 'user', 'content': f'Verifie dans {inventaire} puis repond a la question "{user}"'}
        response = ollama.chat(model='assistant_1', messages=[b])
        print(f"Assistant: {response['message']['content']}")
    else:
        break
