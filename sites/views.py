import logging
import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import WebsiteForm
from .models import Website


logger = logging.getLogger(__name__)


@login_required
def create_website(request):
    if request.method == 'POST':
        form = WebsiteForm(request.POST)
        if form.is_valid():
            new_website = form.save(commit=False)
            new_website.user = request.user
            new_website.save()
            return redirect('website:website_list')
    else:
        form = WebsiteForm()

    return render(request, 'create_website.html', {'form': form})

@login_required
def website_list(request):
    websites = Website.objects.filter(user=request.user)
    return render(request, 'website_list.html', {'websites': websites})


def is_external_link(href, user_site_name):
    parsed_href = urlparse(href)
    return parsed_href.netloc != user_site_name and parsed_href.scheme in ['http', 'https']


def modify_links(content, user_site_name, orig):
    soup = BeautifulSoup(content, 'html.parser')

    for tag in soup.find_all('a', href=True):
        href = tag['href']
        new_href = href.replace(href, f'http://127.0.0.1:8000/sites/{user_site_name}/{orig}{href}')
        tag['href'] = new_href

    return str(soup)


def proxy_view(request, user_site_name, routes_on_original_site):
    try:
        original_site_url = f"https://{user_site_name}.com/{routes_on_original_site}"

        response = requests.get(routes_on_original_site)

        if response.status_code == 200:
            proxied_content = response.content
            website = Website.objects.filter(name=user_site_name)[0]

            modified_content = modify_links(proxied_content, user_site_name, website.url)
            website.increment_clicks()

            website.update_data_sent(len(proxied_content))
            website.update_data_received(len(modified_content))

            return HttpResponse(modified_content)

        else:
            logger.error(f"Request to {original_site_url} failed with status code {response.status_code}")
            return HttpResponse("Помилка під час отримання контенту з оригінального сайту", status=response.status_code)

    except requests.RequestException as e:
        logger.exception("Request to original site failed:")
        return HttpResponse("Помилка під час з'єднання з оригінальним сайтом", status=500)
