from django.shortcuts import render
from django.http import JsonResponse
import requests
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

class MBhJSONViewSet(viewsets.ViewSet):
    BASE_URL = "https://github.com/bhavykhatri/DharmicData/raw/refs/heads/main/Mahabharata/Critical%20Edition/"
    def retrieve_by_key(self,
                        request,
                        lookup=None):
        # Extract volume number and key
        volume=lookup[:2]
        key=lookup

        # Construct full URL for the specific JSON file
        filename = f'MBh{volume}.json'
        full_url = f'{self.BASE_URL}{filename}'

        try:
            # Fetch JSON file
            response = requests.get(full_url)
            response.raise_for_status()
            json_data = response.json()

            # Look for the specific key
            if key in json_data:
                return Response(
                    json_data[key]

                )
            else:
                return Response(
                    {
                        "error": f"{key} not found in {filename}"
                    },
                    status=status.HTTP_404_NOT_FOUND
                )
            
        except requests.exceptions.RequestException:
            return Response(
                {
                    "error": f"Could not fetch{filename}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




def index(request):
    firsts = [
        "Mahābhārata",
        "Veda",
        "Rāmāyaṇa"
    ],
    seconds = {
        "Mahābhārata": [
            "Ādi Parva",
            "Sabhā Parva",
            "Vana Parva",
            "Virāṭa Parva",
            "Udyoga Parva",
            "Bhīṣma Parva",
            "Droṇa Parva",
            "Karṇa Parva",
            "Śalya Parva",
            "Strī Parva",
            "Śānti Parva",
"Anuśāsana Parva",
"Āśramavāsika Parva",
"Āśvamedha Parva",
"Mausala Parva",
"Mahāprasthānika Parva",
"Svargārohaṇa Parva",
"Khilvāṃśa Parva"
        ],
        "Veda": ["R̥gveda", "YajurVeda", "AtharvaVeda"],
        "Rāmāyaṇa": [

    "Bāla Kāṇḍa","Ayodhyā Kāṇḍa",
      "Āraṇya Kāṇḍa","Kiṣkindhā Kāṇḍa",
      "Sundarā Kāṇḍa", "Yuddha Kāṇḍa",
      "Uttara Kāṇḍa"
        ]
    }
    selected_first = request.GET.get('first', '')
    selected_second = request.GET.get('second', '')
    context = {
        'firsts':firsts,
        'seconds': seconds.get(selected_first, []),
        'selected_first':selected_first,
        'selected_second':selected_second
    }
    return render(request, "index.html", context)
