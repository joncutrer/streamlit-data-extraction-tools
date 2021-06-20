import copy
from logging import PlaceHolder
import random
from typing import Dict, List, Literal

import pandas as pd
import streamlit as st
from bs4 import BeautifulSoup

from config import cfg  # loads config from config.yml

st.set_page_config(cfg.app.name, layout=cfg.ui.layout)

query_params: Dict[str, List[str]] = st.experimental_get_query_params()

if query_params.get("m"):
    current_module_slug = query_params["m"][0]
else:
    current_module_slug = ""

st.sidebar.title(cfg.app.name)

st.sidebar.write(cfg.app.tagline)

st.sidebar.markdown(
    '<a target="_blank" href="https://jcutrer.com">jcutrer.com</a> | <a target="_blank" href="https://github.com/joncutrer/streamlit-data-extraction-tools">github</a> | <a target="_blank" href="https://www.buymeacoffee.com/jcutrer">donate</a>',
    unsafe_allow_html=True,
)


def get_module_slugs(mod_list):
    return [tmp_dict["slug"] for tmp_dict in mod_list]


def get_module_texts(mod_list):
    return [tmp_dict["text"] for tmp_dict in mod_list]


def get_module_by_slug(slug, mod_list):
    for dict in mod_list:
        if dict.get("slug") == slug:
            return dict

    return None


def get_module_slug_by_id(id, mod_list):
    for dict in mod_list:
        if dict.get("idx") == id:
            return dict["slug"]
    return ""


def get_module_slug_by_prefix(prefix, mod_list):
    for dict in mod_list:
        if dict.get("text")[:2] == prefix:
            return dict.get("slug")
    return None


def navigate_to(slug):
    st.experimental_set_query_params(m=slug)


module_list_dict = [
    {"idx": 0, "slug": "", "text": "select a module"},
    {"idx": 1, "slug": "html-select-list-extractor", "text": "01: <select> to list"},
    {"idx": 2, "slug": "html-multi-list-extractor", "text": "02: <select> multiple to list"},
    {"idx": 3, "slug": "html-table-to-csv", "text": "10: <table> to csv"},
    {"idx": 4, "slug": "html-link-extractor", "text": "20: <a> Link Extractor"},
    # {"idx": 5, "slug": "ul-list-extractor", "text": "30: <ul> Unordered List Extractor"},
    # {"idx": 6, "slug": "json_prettify", "text": "40: json formatter"},
    # {"idx": 7, "slug": "json-to-csv", "text": "41: json data to csv"},
    # {"idx": 8, "slug": "xml-to-json", "text": "50: xml data to json"},
    # {"idx": 9, "slug": "realtime-regex", "text": "F0: Realtime Regex tester"},
    {"idx": 5, "slug": "docs", "text": "Documentation"},
    {"idx": 6, "slug": "changelog", "text": "CHANGELOG"},
]


selected_module_id = get_module_by_slug(current_module_slug, module_list_dict).get("idx")

# selected_module_id = module_list.index(
#     [i for i in module_list_dict if i.startswith(query_params["m"][0])][0]
# )

# Set page title for selected module

# st.set_page_config(page_title=current_module.get("slug"))


module = st.sidebar.selectbox(
    "Modules",
    get_module_texts(module_list_dict),
    index=selected_module_id,
)

########################
########################
if module[:2] == "01":

    # Change URL
    st.experimental_set_query_params(m=get_module_slug_by_prefix(module[:2], module_list_dict))

    ######## Beging Sidebar ########

    st.sidebar.subheader("Options")

    opt_sample_data = st.sidebar.checkbox("Load Example Data")

    if opt_sample_data == True:
        sample_html = """<select>
<option disabled="">Select one</option>
<option value="A">Choice A</option>
<option value="B">Choice B</option>
<option value="C">Choice C</option>
<option value="D">Choice D</option>
<option value="E">Choice E</option>
<option value="F">Choice F</option>
</select>"""

    else:
        sample_html = ""

    opt_exclude_disabled = st.sidebar.checkbox("Exclude Disabled Elements")

    opt_return_data = st.sidebar.radio("Return Data", ["Text", "Value", "Value+Text"])

    if opt_return_data == "Value+Text":

        opt_value_sep = st.sidebar.text_input(
            "Value+Text Seperator",
            value=",",
            max_chars=8,
            key=7392857982,
        )

    opt_item_sep = st.sidebar.selectbox(
        "Item delimiter", ["\\n Newline", "\\t Tab", ", Comma", "; Semicolon", "| Pipe"]
    )

    if opt_item_sep == "\\n Newline":
        item_sep = "\n"
    elif opt_item_sep == "\\t Tab":
        item_sep = "\t"
    elif opt_item_sep == ", Comma":
        item_sep = ","
    elif opt_item_sep == "; Semicolon":
        item_sep = ";"
    elif opt_item_sep == "| Pipe":
        item_sep = "|"

    opt_prepend = st.sidebar.checkbox(
        "Prepend Text", help="Prepend text to each item", key=3546789876
    )

    if opt_prepend:
        opt_prepend_text = st.sidebar.text_input("", key=687632123)

    opt_append = st.sidebar.checkbox(
        "Append Text", help="Append text to each item", key=7876542245
    )

    if opt_append:
        opt_append_text = st.sidebar.text_input("", key=3456787123)

    ######## End  Sidebar ########

    ######## Begin Main Window ########

    st.header("Module " + module)
    st.write(
        "This simple tool will will transform an html <select> code block into a simple list."
    )

    target_html = st.text_area(
        "Paste <select> HTML here", sample_html, height=cfg.ui.textarea_height
    )

    btn_go = st.button("Go")

    if target_html != "":
        try:
            soup = BeautifulSoup(target_html, "html.parser")

            data_list = []
            for item in soup.find("select").find_all("option"):
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

            output = st.text_area("Output", item_sep.join(data_list), cfg.ui.textarea_height)
        except Exception as e:
            st.write(
                '<span style="color:red">An error occured while parsing your input.  Check for missing html tags.</span>',
                unsafe_allow_html=True,
            )
            st.write(e)


########################
########################
elif module[:2] == "02":

    # Change URL
    st.experimental_set_query_params(m=get_module_slug_by_prefix(module[:2], module_list_dict))

    ######## Beging Sidebar ########
    st.sidebar.subheader("Options")

    # Load sidebar options

    opt_sample_data = st.sidebar.checkbox("Load Example Data")

    if opt_sample_data == True:
        sample_html = """<select name="Month">
<option disabled="">- Month -</option>
<option value="01">January</option>
<option value="02">Febuary</option>
<option value="03">March</option>
<option value="04">April</option>
<option value="05">May</option>
<option value="06">June</option>
<option value="07">July</option>
<option value="08">August</option>
<option value="09">September</option>
<option value="10">October</option>
<option value="11">November</option>
<option value="12">December</option>
</select>

<select name="Year">
<option disabled="">- Year -</option>
<option value="2021">2021</option>
<option value="2020">2020</option>
<option value="2019">2019</option>
<option value="2018">2018</option>
<option value="2017">2017</option>
</select>"""

    else:
        sample_html = ""

    opt_exclude_disabled = st.sidebar.checkbox("Exclude Disabled Elements")

    opt_return_data = st.sidebar.radio("Return Data", ["Text", "Value", "Value+Text"])

    if opt_return_data == "Value+Text":

        opt_value_sep = st.sidebar.text_input("Value+Text Seperator", value=",", max_chars=8)

    opt_prepend = st.sidebar.checkbox("Prepend Text")

    if opt_prepend:
        opt_prepend_text = st.sidebar.text_input("", key=4324243232)

    opt_append = st.sidebar.checkbox("Append Text")

    if opt_append:
        opt_append_text = st.sidebar.text_input(
            "", help="Text that will be appended to each line of the list", key=1298329843
        )

    st.header("Module " + module)
    st.write(
        "This tool will takes a block of html containing multiple <select> elements and parse all each as separate lists or a combined list."
    )

    target_html = st.text_area(
        "Paste <select> HTML here", sample_html, height=cfg.ui.textarea_height
    )

    btn_go = st.button("Go")

    if target_html != "":

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

                for item in el.find_all("option"):

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
                    data_list_combined.append(item_str)

                st.text_area(
                    f"{str(len(data_list))} Items",
                    "\n".join(data_list),
                    cfg.ui.textarea_height,
                    key=random.randint(0, 999999999),
                )

            st.subheader(f"All lists combined")
            st.text_area(
                f"{str(len(data_list_combined))} Items",
                "\n".join(data_list_combined),
                cfg.ui.textarea_height,
                key=2347328943743,
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

    # Change URL
    st.experimental_set_query_params(m=get_module_slug_by_prefix(module[:2], module_list_dict))

    ######## Beging Sidebar ########
    st.sidebar.subheader("Options")

    # Load sidebar options
    opt_sample_data = st.sidebar.checkbox("Load Example Data")

    if opt_sample_data == True:
        sample_html = """<table class="table table-bordered table-hover table-condensed">
<thead><tr><th title="Field #1">id</th>
<th title="Field #2">name</th>
<th title="Field #3">amount</th>
<th title="Field #4">Remark</th>
</tr></thead>
<tbody><tr>
<td align="right">1</td>
<td>Johnson, Smith, and Jones Co.</td>
<td align="right">345.33</td>
<td>Pays on time</td>
</tr>
<tr>
<td align="right">2</td>
<td>Sam &quot;Mad Dog&quot; Smith</td>
<td align="right">993.44</td>
<td> </td>
</tr>
<tr>
<td align="right">3</td>
<td>Barney &amp; Company</td>
<td align="right">0</td>
<td>Great to work with<br/>and always pays with cash.</td>
</tr>
<tr>
<td align="right">4</td>
<td>Johnson&#39;s Automotive</td>
<td align="right">2344</td>
<td> </td>
</tr>
</tbody></table>"""

    else:
        sample_html = ""

    opt_header_row = st.sidebar.checkbox("1st row contains column names", value=True)

    st.header("Module " + module)
    st.write(
        "This tool will takes a block of html containing a <table> and converts the data to csv format"
    )

    target_html = st.text_area(
        "Paste <table> HTML here", sample_html, height=cfg.ui.textarea_height
    )

    btn_go = st.button("Go")

    if target_html != "":

        try:
            soup = BeautifulSoup(target_html, "html.parser")

            table_el = soup.find("table")
            st.write("HTML Length: " + str(len(target_html)))

            data_list_combined = []

            rows = table_el.findAll("tr")
            data_rows = []
            for row in rows:
                csv_row = []
                for cell in row.findAll(["td", "th"]):
                    csv_row.append(cell.get_text().strip())

                data_rows.append(csv_row)

            if opt_header_row:
                tabledata_df = pd.DataFrame(data_rows[1:], columns=data_rows[0])
                tabledata_csv = tabledata_df.to_csv(
                    sep=",", quoting=1, line_terminator="\r\n", doublequote=True, escapechar="\\"
                )
            else:
                tabledata_df = pd.DataFrame(data_rows)
                tabledata_csv = tabledata_df.to_csv(
                    sep=",",
                    quoting=1,
                    header=False,
                    line_terminator="\r\n",
                    doublequote=True,
                    escapechar="\\",
                )

            st.write(f"{str(len(tabledata_df))} Items")
            # Output interim dataframe
            st.write(tabledata_df)

            st.subheader(f"CSV Output")
            st.text_area(
                f"{str(len(tabledata_df))} Items",
                tabledata_csv,
                cfg.ui.textarea_height,
                key=2347890043,
            )

        except Exception as e:
            st.write(
                '<span style="color:red">An error occured while parsing your input.  Check for missing html tags.</span>',
                unsafe_allow_html=True,
            )
            st.write(e)


########################
########################
elif module[:2] == "20":

    # Change URL
    st.experimental_set_query_params(m=get_module_slug_by_prefix(module[:2], module_list_dict))

    ######## Beging Sidebar ########
    st.sidebar.subheader("Options")

    # Load sidebar options
    opt_sample_data = st.sidebar.checkbox("Load Example Data")

    if opt_sample_data == True:
        sample_html = """<div class="tab-pane active" id="top-500-domains">
      <div class="mt-5 mb-3">
	    <div class="cta-wrapper"><a class="" href="/top-500/download/?table=top500Domains" download="">Download the Top 500 Domains as a CSV</a></div>
      </div>
      <table class="table table-responsive-md table-bordered table-zebra mb-5">
      <thead><tr><th>Rank</th><th>Root Domain</th><th>Linking Root Domains</th><th>Domain Authority</th></tr></thead>
      <tbody translate="no">
      <tr><td>1</td><td><a href="http://youtube.com">youtube.com</a></td><td>19,186,340</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 100%;">100</div></div></td></tr>
      <tr><td>2</td><td><a href="http://apple.com">apple.com</a></td><td>6,131,103</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 100%;">100</div></div></td></tr>
      <tr><td>3</td><td><a href="http://www.google.com">www.google.com</a></td><td>12,585,136</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 100%;">100</div></div></td></tr>
      <tr><td>4</td><td><a href="http://microsoft.com">microsoft.com</a></td><td>4,562,755</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 99%;">99</div></div></td></tr>
      <tr><td>5</td><td><a href="http://play.google.com">play.google.com</a></td><td>4,007,864</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 99%;">99</div></div></td></tr>
      <tr><td>6</td><td><a href="http://cloudflare.com">cloudflare.com</a></td><td>5,245,716</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 99%;">99</div></div></td></tr>
      <tr><td>7</td><td><a href="http://support.google.com">support.google.com</a></td><td>4,581,827</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 99%;">99</div></div></td></tr>
      <tr><td>8</td><td><a href="http://www.blogger.com">www.blogger.com</a></td><td>26,381,101</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 99%;">99</div></div></td></tr>
      <tr><td>9</td><td><a href="http://mozilla.org">mozilla.org</a></td><td>1,887,822</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 98%;">98</div></div></td></tr>
      <tr><td>10</td><td><a href="http://wordpress.org">wordpress.org</a></td><td>10,766,082</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 98%;">98</div></div></td></tr>
      <tr><td>11</td><td><a href="http://linkedin.com">linkedin.com</a></td><td>9,850,153</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 98%;">98</div></div></td></tr>
      <tr><td>12</td><td><a href="http://docs.google.com">docs.google.com</a></td><td>2,540,199</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 98%;">98</div></div></td></tr>
      <tr><td>13</td><td><a href="http://youtu.be">youtu.be</a></td><td>4,058,192</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 98%;">98</div></div></td></tr>
      <tr><td>14</td><td><a href="http://en.wikipedia.org">en.wikipedia.org</a></td><td>5,777,161</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 98%;">98</div></div></td></tr>
      <tr><td>15</td><td><a href="http://maps.google.com">maps.google.com</a></td><td>4,571,921</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 98%;">98</div></div></td></tr>
      <tr><td>16</td><td><a href="http://plus.google.com">plus.google.com</a></td><td>11,903,181</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 97%;">97</div></div></td></tr>
      <tr><td>17</td><td><a href="http://vimeo.com">vimeo.com</a></td><td>3,155,384</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 97%;">97</div></div></td></tr>
      <tr><td>18</td><td><a href="http://europa.eu">europa.eu</a></td><td>1,666,354</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 97%;">97</div></div></td>
      </tr><tr><td>19</td><td><a href="http://googleusercontent.com">googleusercontent.com</a></td><td>2,236,257</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 97%;">97</div></div></td></tr>
      <tr><td>20</td><td><a href="http://drive.google.com">drive.google.com</a></td><td>1,868,734</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 97%;">97</div></div></td></tr>
      <tr><td>21</td><td><a href="http://sites.google.com">sites.google.com</a></td><td>1,825,514</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 97%;">97</div></div></td></tr>
      <tr><td>22</td><td><a href="http://adobe.com">adobe.com</a></td><td>2,718,808</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 97%;">97</div></div></td></tr>
      <tr><td>23</td><td><a href="http://accounts.google.com">accounts.google.com</a></td><td>2,501,041</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 97%;">97</div></div></td></tr>
      <tr><td>24</td><td><a href="http://istockphoto.com">istockphoto.com</a></td><td>3,193,178</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 96%;">96</div></div></td></tr>
      <tr><td>25</td><td><a href="http://es.wikipedia.org">es.wikipedia.org</a></td><td>816,985</td><td><div class="progress"><div class="progress-bar bg-success" style="width: 96%;">96</div></div></td></tr>
      </tbody>
      </table>
 </div>"""

    else:
        sample_html = ""

    opt_exclude_anchor = st.sidebar.checkbox("Exclude anchor links")

    opt_exclude_relative = st.sidebar.checkbox("Exclude relative links")

    opt_return_data = st.sidebar.radio("Return Data", ["Text", "URL", "Text+URL"])

    if opt_return_data == "Text+URL":

        opt_value_sep = st.sidebar.text_input(
            "Text+URL Seperator",
            value=",",
            max_chars=8,
            key=7392251902,
        )

    st.header("Module " + module)
    st.write(
        'This tool will takes a block of html containing multiple <a href=""> elements and parse links into a list.'
    )

    target_html = st.text_area(
        "Paste <select> HTML here", sample_html, height=cfg.ui.textarea_height
    )

    btn_go = st.button("Go")

    if target_html != "":

        try:
            soup = BeautifulSoup(target_html, "html.parser")

            els = soup.find_all("a")
            st.write("HTML Length: " + str(len(target_html)))
            st.write("<a> elements found: " + str(len(els)))

            el_counter = 0

            data_list_combined = []

            link_list = []
            for el in els:
                href = el.get("href")
                if href == None:
                    continue
                if len(href) < 1:
                    continue
                if opt_exclude_anchor:
                    if href[:1] == "#":
                        continue

                if opt_exclude_relative:
                    if href[:1] == "/" or href[:1] == ".":
                        continue

                if opt_return_data == "Text":
                    link_list.append(el.get_text())
                elif opt_return_data == "URL":
                    link_list.append(el.get("href"))
                elif opt_return_data == "Text+URL":
                    link_list.append(el.get_text() + opt_value_sep + el.get("href"))

                el_counter += 1
                # st.subheader(f"Link {el_counter}")
                # st.write(el.get("href"))

            st.subheader(f"Output")
            st.text_area(
                f"{str(len(link_list))} Items",
                "\n".join(link_list),
                cfg.ui.textarea_height,
                key=2438904343233,
            )

        except Exception as e:
            st.write(
                '<span style="color:red">An error occured while parsing your input.  Check for missing html tags.</span>',
                unsafe_allow_html=True,
            )
            st.write(e)


########################
########################
elif module[:2] == "30":

    # Change URL
    st.experimental_set_query_params(m=get_module_slug_by_prefix(module[:2], module_list_dict))

    ######## Beging Sidebar ########
    st.sidebar.subheader("Options")

    # Load sidebar options

    opt_sample_data = st.sidebar.checkbox("Load Example Data")

    st.header("Module " + module)
    st.write("- nothing here yet -")

########################
########################
elif module[:2] == "40":

    # Change URL
    st.experimental_set_query_params(m=get_module_slug_by_prefix(module[:2], module_list_dict))

    ######## Beging Sidebar ########
    st.sidebar.subheader("Options")

    # Load sidebar options

    opt_sample_data = st.sidebar.checkbox("Load Example Data")

    st.header("Module " + module)


########################
########################
elif module == "Documentation":

    # Change URL
    st.experimental_set_query_params(m=get_module_slug_by_prefix(module[:2], module_list_dict))

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

    # Change URL
    st.experimental_set_query_params(m=get_module_slug_by_prefix(module[:2], module_list_dict))

    st.header("CHANGELOG")

    st.markdown(
        """
* 2021-06-20 Added Module 20 <a> link extractor
* 2021-06-19 Added Module 10 html table to csv
* 2021-04-13 Added Modules 01 & 02 html select extractor
* 2021-04-12 Project Inception"""
    )


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
<p style="font-size:2em; font-family: monospace; color: #20a5e4;">{call_to_action[random_cta]}</p>
<a href="https://www.buymeacoffee.com/jcutrer" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="width:50%;max-width: 420px;" ></a>
</center>
<br>
<p><center><small>--- streamlit app by <a href="https://jcutrer.com">JC</a> ---</small></center></p>
"""

st.write(page_footer, unsafe_allow_html=True)