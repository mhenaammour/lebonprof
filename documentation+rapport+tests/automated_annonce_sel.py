from django.test import TestCase

#Create your tests here.#
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

#initialisation du navigateur web#
profile = webdriver.FirefoxProfile('/home/mhena/snap/firefox/common/.cache/mozilla/firefox/7mqeradx.default')
driver = webdriver.Firefox(firefox_profile=profile)
#navigation vers la page de connexion#
driver.get("http://localhost:8000/login/")

#saisie des informations de connexion#
username = driver.find_element_by_name("username")
username.send_keys("mhena")
password = driver.find_element_by_name("password")
password.send_keys("mhennario")

#clic sur le bouton de connexion#
driver.find_element_by_name("LOGIN").click()

#attente pour la redirection vers la page "mon compte#"
time.sleep(3)

#clic sur le bouton "Mes annonces#
driver.get("http://localhost:8000/mesannonces/")

#attente pour la redirection vers la page de publication d'annonce#
time.sleep(3)
driver.find_element_by_name("Publier Annonce").click()

#saisie des informations de l'annonce#
driver.find_element_by_name("title").send_keys("maths")
driver.find_element_by_name("category").send_keys("primaire")
driver.find_element_by_name("modalite").send_keys("Online")
driver.find_element_by_name("theme").send_keys("Maths")
driver.find_element_by_name("description").send_keys("Description de l'annonce")
driver.find_element_by_name("tarif").send_keys("1222")
driver.find_element_by_name("wilaya").send_keys("Alger")
driver.find_element_by_name("addresse").send_keys("Adresse")
driver.find_element_by_name("commune").send_keys("wled fayet")

# clic sur le bouton "Publier#"
driver.find_element_by_name("PUBLIER").click()

#attente pour la publication de l'annonce#
time.sleep(5)

#fermeture du navigateur web#
driver.quit()


