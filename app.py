import copy
from logging import PlaceHolder
import random

import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

import extras


st.sidebar.title("JC's Data Extraction Tools")

st.sidebar.write("Created with Streamlit by JC")

st.sidebar.markdown(
    '<a target="_blank" href="https://jcutrer.com">jcutrer.com</a> | <a target="_blank" href="https://github.com/joncutrer">github</a>',
    unsafe_allow_html=True,
)


module = st.sidebar.selectbox(
    "Modules",
    [
        "select a module",
        "01: <select> to list",
        "02: Multiple <select> parsing",
        "10: <table> to csv",
        "20: <a> Link Extractor",
        "30: <ul> Unordered List Extractor",
        "40: json formatter",
        "41: json data to csv",
        "50: xml data to json",
        "F0: Realtime Regex tester",
        "Documentation",
        "CHANGELOG",
    ],
)

########################
########################
if module[:2] == "01":

    st.header("Module " + module)
    st.write("This simple tool will take html <select> code block and return as a list.")
    # Load sidebar options

    st.sidebar.subheader("Options")
    opt_sample_data = st.sidebar.checkbox("Load Example Data")

    if opt_sample_data == True:
        sample_html = """<select aria-label="Make" placeholder="Make" class="css-1h5kne3-StyledSelect e1lpma6w4" aria-labelledby="makeSelectLabel"><option selected="" value="" disabled="">Make</option><option value="Acura">Acura</option><option value="Aston Martin">Aston Martin</option><option value="Audi">Audi</option><option value="Bentley">Bentley</option><option value="BMW">BMW</option><option value="Buick">Buick</option><option value="Cadillac">Cadillac</option><option value="Chevrolet">Chevrolet</option><option value="Chrysler">Chrysler</option><option value="Dodge">Dodge</option><option value="Ford">Ford</option><option value="GMC">GMC</option><option value="Honda">Honda</option><option value="HUMMER">HUMMER</option><option value="Hyundai">Hyundai</option><option value="INFINITI">INFINITI</option><option value="Isuzu">Isuzu</option><option value="Jaguar">Jaguar</option><option value="Jeep">Jeep</option><option value="Kia">Kia</option><option value="Land Rover">Land Rover</option><option value="Lexus">Lexus</option><option value="Lincoln">Lincoln</option><option value="Lotus">Lotus</option><option value="Maserati">Maserati</option><option value="Maybach">Maybach</option><option value="MAZDA">MAZDA</option><option value="Mercedes-Benz">Mercedes-Benz</option><option value="Mercury">Mercury</option><option value="MINI">MINI</option><option value="Mitsubishi">Mitsubishi</option><option value="Nissan">Nissan</option><option value="Panoz">Panoz</option><option value="Pontiac">Pontiac</option><option value="Porsche">Porsche</option><option value="Rolls-Royce">Rolls-Royce</option><option value="Saab">Saab</option><option value="Saturn">Saturn</option><option value="Scion">Scion</option><option value="Subaru">Subaru</option><option value="Suzuki">Suzuki</option><option value="Toyota">Toyota</option><option value="Volkswagen">Volkswagen</option><option value="Volvo">Volvo</option></select>
    """
    else:
        sample_html = ""

    opt_exclude_disabled = st.sidebar.checkbox("Exclude Disabled Elements")

    opt_return_data = st.sidebar.radio("Return Data", ["Text", "Value", "Value+Text"])

    if opt_return_data == "Value+Text":

        opt_value_sep = st.sidebar.text_input("Value+Text Seperator", value=",", max_chars=8)

    opt_prepend = st.sidebar.checkbox("Prepend Text")

    if opt_prepend:
        opt_prepend_text = st.sidebar.text_input("")

    opt_append = st.sidebar.checkbox("Append Text")

    if opt_append:
        opt_append_text = st.sidebar.text_input(
            "", help="Text that will be appended to each line of the list"
        )

    # End Sidebar
    # Begin Main Window

    target_html = st.text_area("Paste <select> HTML here", sample_html, height=300)

    btn_go = st.button("Go")

    if target_html != "":
        try:
            soup = BeautifulSoup(target_html, "html.parser")

            data_list = []
            for item in soup.find("select"):
                item_str = ""

                if opt_prepend:
                    item_str += opt_prepend_text

                # If exclude disabled items if option is set
                if opt_exclude_disabled & item.has_attr("disabled"):
                    continue

                if opt_return_data == "Value":
                    if item.has_attr("value"):
                        item_str += item["value"]

                elif opt_return_data == "Value+Text":

                    if item.has_attr("value"):
                        item_str += item["value"]

                    if opt_value_sep:
                        item_str += opt_value_sep

                    item_str += item.text

                elif opt_return_data == "Text":
                    item_str += item.text

                if opt_append:
                    item_str += opt_append_text

                data_list.append(item_str)

            st.write("HTML Length: " + str(len(target_html)))
            st.write("List Items: " + str(len(data_list)))

            output = st.text_area("Output", "\n".join(data_list), 400)
        except Exception as e:
            st.write(
                '<span style="color:red">An error occured while parsing your input.  Check for missing html tags.</span>',
                unsafe_allow_html=True,
            )
            st.write(e)


########################
########################
elif module[:2] == "02":

    st.header("Module " + module)
    st.write(
        "This tool will takes a block of html containing multiple <select> elements and parse all each as separate lists or a combined list."
    )
    # Load sidebar options

    opt_sample_data = st.sidebar.checkbox("Load Example Data")

    opt_exclude_disabled = st.sidebar.checkbox("Exclude Disabled Elements")

    opt_value_instead = st.sidebar.checkbox("Use value= instead of text")

    opt_value_plus_text = st.sidebar.checkbox("Return value= + text")

    if opt_sample_data == True:
        sample_html = """<div class="css-13qjaow-Content e1fqxqny0"><div><p type="body" class="css-q8ngks-StyledParagraph e12faeex0">New cars, Certified Pre-Owned (CPO) cars, used cars – we’ll show you what you should expect to pay.</p></div><div class="css-nzb090 ep157qi0"><form action="" class="css-et6ctm-DefaultForm-defaultFormStyles-defaultPrivacyPolicyStyles-defaultEmailInputStyles e1x4b5ct0"><div class="year"><div class="css-18gpyz4-SelectWrapper-VehiclePickerInput e1lpma6w3" id=""><select aria-label="Year" placeholder="Year" class="css-1h5kne3-StyledSelect e1lpma6w4" aria-labelledby="yearSelectLabel"><option selected="" value="" disabled="">Year</option><option value="2022">2022</option><option value="2021">2021</option><option value="2020">2020</option><option value="2019">2019</option><option value="2018">2018</option><option value="2017">2017</option><option value="2016">2016</option><option value="2015">2015</option><option value="2014">2014</option><option value="2013">2013</option><option value="2012">2012</option><option value="2011">2011</option><option value="2010">2010</option><option value="2009">2009</option><option value="2008">2008</option><option value="2007">2007</option><option value="2006">2006</option><option value="2005">2005</option><option value="2004">2004</option><option value="2003">2003</option><option value="2002">2002</option><option value="2001">2001</option><option value="2000">2000</option><option value="1999">1999</option><option value="1998">1998</option><option value="1997">1997</option><option value="1996">1996</option><option value="1995">1995</option><option value="1994">1994</option><option value="1993">1993</option><option value="1992">1992</option></select><label id="yearSelectLabel" class="placeholder-label css-xrpr7x-PopulatedPlaceholder e1lpma6w0">Year</label><div class="css-omvzla-Carot e1lpma6w2"><svg size="18" color="darkBrightBlue" x="0px" y="0px" viewBox="0 0 64 64" class="css-1v441j5-StyledIcon e1vcxgeb0"><g><defs><polygon points="-507,-1597.791 -508.209,-1599 -513,-1594.209 -517.791,-1599 -519,-1597.791 -514.209,-1593 -519,-1588.209 -517.791,-1587 -513,-1591.791 -508.209,-1587 -507,-1588.209 -511.791,-1593 		"></polygon></defs><g><defs><rect x="-688" y="-3317" width="1440" height="6698"></rect></defs></g></g><g><polyline fill="none" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" points="56.976,22.03 31.414,47.592 5.852,22.03 	"></polyline></g></svg></div></div></div><div class="make"><div class="css-18gpyz4-SelectWrapper-VehiclePickerInput e1lpma6w3" id=""><select aria-label="Make" placeholder="Make" class="css-1h5kne3-StyledSelect e1lpma6w4" aria-labelledby="makeSelectLabel"><option selected="" value="" disabled="">Make</option><option value="Acura">Acura</option><option value="Aston Martin">Aston Martin</option><option value="Audi">Audi</option><option value="Bentley">Bentley</option><option value="BMW">BMW</option><option value="Buick">Buick</option><option value="Cadillac">Cadillac</option><option value="Chevrolet">Chevrolet</option><option value="Chrysler">Chrysler</option><option value="Dodge">Dodge</option><option value="Ford">Ford</option><option value="GMC">GMC</option><option value="Honda">Honda</option><option value="HUMMER">HUMMER</option><option value="Hyundai">Hyundai</option><option value="INFINITI">INFINITI</option><option value="Isuzu">Isuzu</option><option value="Jaguar">Jaguar</option><option value="Jeep">Jeep</option><option value="Kia">Kia</option><option value="Land Rover">Land Rover</option><option value="Lexus">Lexus</option><option value="Lincoln">Lincoln</option><option value="Lotus">Lotus</option><option value="Maserati">Maserati</option><option value="Maybach">Maybach</option><option value="MAZDA">MAZDA</option><option value="Mercedes-Benz">Mercedes-Benz</option><option value="Mercury">Mercury</option><option value="MINI">MINI</option><option value="Mitsubishi">Mitsubishi</option><option value="Nissan">Nissan</option><option value="Panoz">Panoz</option><option value="Pontiac">Pontiac</option><option value="Porsche">Porsche</option><option value="Rolls-Royce">Rolls-Royce</option><option value="Saab">Saab</option><option value="Saturn">Saturn</option><option value="Scion">Scion</option><option value="Subaru">Subaru</option><option value="Suzuki">Suzuki</option><option value="Toyota">Toyota</option><option value="Volkswagen">Volkswagen</option><option value="Volvo">Volvo</option></select><label id="makeSelectLabel" class="placeholder-label css-xrpr7x-PopulatedPlaceholder e1lpma6w0">Make</label><div class="css-omvzla-Carot e1lpma6w2"><svg size="18" color="darkBrightBlue" x="0px" y="0px" viewBox="0 0 64 64" class="css-1v441j5-StyledIcon e1vcxgeb0"><g><defs><polygon points="-507,-1597.791 -508.209,-1599 -513,-1594.209 -517.791,-1599 -519,-1597.791 -514.209,-1593 -519,-1588.209 -517.791,-1587 -513,-1591.791 -508.209,-1587 -507,-1588.209 -511.791,-1593 		"></polygon></defs><g><defs><rect x="-688" y="-3317" width="1440" height="6698"></rect></defs></g></g><g><polyline fill="none" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" points="56.976,22.03 31.414,47.592 5.852,22.03 	"></polyline></g></svg></div></div></div><div class="model"><div class="css-18gpyz4-SelectWrapper-VehiclePickerInput e1lpma6w3" id=""><select aria-label="Model" placeholder="Model" class="css-yjufmi-StyledSelect e1lpma6w4"><option selected="" value="" disabled="">Model</option><option value="4Runner">4Runner</option><option value="Avalon">Avalon</option><option value="Camry">Camry</option><option value="Celica">Celica</option><option value="Corolla">Corolla</option><option value="Echo">Echo</option><option value="Highlander">Highlander</option><option value="Land Cruiser">Land Cruiser</option><option value="Matrix">Matrix</option><option value="MR2">MR2</option><option value="Prius">Prius</option><option value="RAV4">RAV4</option><option value="Sequoia">Sequoia</option><option value="Sienna">Sienna</option><option value="Solara">Solara</option><option value="Tacoma Access Cab">Tacoma Access Cab</option><option value="Tacoma Double Cab">Tacoma Double Cab</option><option value="Tacoma Regular Cab">Tacoma Regular Cab</option><option value="Tundra Access Cab">Tundra Access Cab</option><option value="Tundra Double Cab">Tundra Double Cab</option><option value="Tundra Regular Cab">Tundra Regular Cab</option></select><div class="css-omvzla-Carot e1lpma6w2"><svg size="18" color="darkBrightBlue" x="0px" y="0px" viewBox="0 0 64 64" class="css-1v441j5-StyledIcon e1vcxgeb0"><g><defs><polygon points="-507,-1597.791 -508.209,-1599 -513,-1594.209 -517.791,-1599 -519,-1597.791 -514.209,-1593 -519,-1588.209 -517.791,-1587 -513,-1591.791 -508.209,-1587 -507,-1588.209 -511.791,-1593 		"></polygon></defs><g><defs><rect x="-688" y="-3317" width="1440" height="6698"></rect></defs></g></g><g><polyline fill="none" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" points="56.976,22.03 31.414,47.592 5.852,22.03 	"></polyline></g></svg></div></div></div><button width="auto" href="#" disabled="" type="submit" data-analytics="research_advisor" data-analytics-type="click" class="css-1ib0bnv-commonStyle-default-primary-WrappedButton" target="_self"><span width="auto" disabled="" class="css-20qcuk-primaryButton-primary">Next</span></button></form></div></div>
"""
    else:
        sample_html = ""

    target_html = st.text_area("Paste <select> HTML here", sample_html, height=300)

    btn_go = st.button("Go")

    if target_html != "":

        if btn_go == True:
            # st.write("Button was pushed")

            try:
                soup = BeautifulSoup(target_html, "html.parser")

                select_els = soup.find_all("select")
                st.write("HTML Length: " + str(len(target_html)))
                st.write("<select> elements found: " + str(len(select_els)))

                el_counter = 0

                data_list_combined = []

                for el in select_els:
                    el_counter += 1
                    st.subheader(f"List {el_counter}")

                    tmp_el = copy.copy(el)
                    tmp_el.clear()
                    st.write(tmp_el.encode())
                    data_list = []

                    for item in el:
                        data_list.append(item.text)
                        data_list_combined.append(item.text)

                    # st.write("List Items: " + str(len(data_list)))

                    st.text_area(
                        f"{str(len(data_list))} Items",
                        "\n".join(data_list),
                        400,
                        key=random.randint(1, 999999999),
                    )

                st.subheader(f"All lists combined")
                st.text_area(
                    f"{str(len(data_list_combined))} Items",
                    "\n".join(data_list_combined),
                    400,
                    key=random.randint(1, 999999999),
                )

            except Exception as e:
                st.write(
                    '<span style="color:red">An error occured while parsing your input.  Check for missing html tags.</span>',
                    unsafe_allow_html=True,
                )
                st.write(e)


########################
########################
elif module[:2] == "10":

    st.header("Module " + module)
    # Load sidebar options

    opt_sample_data = st.sidebar.checkbox("Show Example")


########################
########################
elif module[:2] == "20":

    st.header("Module " + module)
    # Load sidebar options

    opt_sample_data = st.sidebar.checkbox("Show Example")


########################
########################
elif module[:2] == "30":

    st.header("Module " + module)
    # Load sidebar options

    opt_sample_data = st.sidebar.checkbox("Show Example")


########################
########################
elif module[:2] == "40":

    st.header("Module " + module)
    # Load sidebar options

    opt_sample_data = st.sidebar.checkbox("Show Example")


########################
########################
elif module == "Documentation":
    st.header("Welcome to the App")

    st.markdown(
        """To get started choose a module from the left sidebar dropdown
or to learn about the available modules keep reading.

### Module 01: <select> to list

### Module 02: Multiple <select> parsing

### Module 10: <table> to csv")

### Module 20: <a> Link Extractor

### Module 30: <ul> Unordered List Extractor

### Module 40: json formatter

### Module 41: json data to csv

### Module 50: xml data to json

### Module 60: blank

### Module 70: blank

### Module 80: blank

### Module 90: blank

### Module a0: blank

### Module b0: blank

### Module c0: blank

### Module d0: blank

### Module e0: blank

### Module f0: blank
"""
    )


######## Begin CHANGELOG ########
elif module == "CHANGELOG":
    st.header("CHANGELOG")

    st.markdown("- nothing here yet -")


######## Begin Page Footer ########

from datetime import datetime

call_to_action = [
    "Is this tool a timesaver for you?",
    "Exactly what you needed?",
    "This software is 100% FREE?",
    "Support the Developer of this tool",
    "Want to say THANK YOU?",
]

random.seed(datetime.now())
random_cta = random.randint(0, len(call_to_action) - 1)

page_footer = f"""
<hr>
<center>
<p style="font-size:3em; font-family: 'Brush Script MT', cursive;">{call_to_action[random_cta]}</p>
<a href="https://www.buymeacoffee.com/jcutrer" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
</center>
<br>
<p><center><small>--- streamlit app by <a href="https://jcutrer.com">JC</a> ---</small></center></p>
"""

st.write(page_footer, unsafe_allow_html=True)