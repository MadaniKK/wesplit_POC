import pytesseract
import cv2


# Function to extract text from the image using Tesseract OCR
def extract_text_from_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(image)

    return text


# Function to parse extracted text into items and prices
def parse_receipt_text(receipt_text):
    items = []
    lines = receipt_text.splitlines()

    for line in lines:
        parts = line.rsplit(" ", 1)
        if len(parts) == 2:
            item_name = parts[0].strip()
            try:
                item_price = float(parts[1].strip())
                items.append((item_name, item_price))
            except ValueError:
                continue

    return items


# Function to assign items to people
def assign_items_to_people(items, people):
    assignments = {person: [] for person in people}

    for item, price in items:
        print(f"\nItem: {item}, Price: ${price}")
        for i, person in enumerate(people):
            print(f"{i+1}. {person}")
        choice = int(input("Who ordered this item? (Enter number): "))
        if 1 <= choice <= len(people):
            assignments[people[choice - 1]].append((item, price))

    return assignments


# Function to calculate the total amount for each person
def calculate_totals(assignments):
    totals = {}
    for person, items in assignments.items():
        totals[person] = sum(price for _, price in items)
    return totals


# Main function to run the POC
def main():
    # Path to the receipt image
    image_path = input("Enter the path to the receipt image: ")

    # Extract text from image
    receipt_text = extract_text_from_image(image_path)
    print("\nExtracted Text:\n", receipt_text)

    # Parse the receipt text to get items and prices
    items = parse_receipt_text(receipt_text)
    print("\nParsed Items:")
    for item, price in items:
        print(f"{item}: ${price}")

    # Get the names of people involved
    people = input(
        "\nEnter the names of the people involved (comma-separated): "
    ).split(",")

    # Assign items to people
    assignments = assign_items_to_people(items, people)

    # Calculate totals for each person
    totals = calculate_totals(assignments)

    # Output the result
    print("\nFinal Totals:")
    for person, total in totals.items():
        print(f"{person}: ${total:.2f}")


if __name__ == "__main__":
    main()
