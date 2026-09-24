# Power BI Screenshot Exporter

> Automate Power BI report screenshot capture using Python and Playwright.

A Python-based browser automation project for capturing screenshots of **public Power BI reports** and saving each report page as an image.

This project started while I was exploring **Python and Playwright**. I had an idea:

> **Can I automate the process of taking screenshots of Power BI report pages?**

That small experiment turned into two different versions of the tool.

---

## ✨ Features

* 🔗 Power BI URL validation
* 🌐 Opens public Power BI reports
* 🖥️ 1920 × 1080 browser viewport
* 📸 PNG screenshot capture
* 🔢 Automatic screenshot numbering
* 📁 Automatic output-folder creation
* ⏱️ Configurable waiting time
* 🎨 Additional rendering support for Power BI/custom visuals
* 🤖 Automatic page navigation in Version 2
* 🛑 Page-change detection
* 🔁 Previously visited page detection

---

# 🖱️ Version 1 — Manual Navigation

[View Manual Version](PowerBI_Capture_Manual.py)

```text
powerbi_screenshot_manual.py
```

The first version gives you **full control over page navigation**.

You enter the public Power BI report URL and manually navigate through the report pages. The script handles the screenshot capture and file naming.

### When is this useful?

The manual version is useful when:

* Your Power BI report contains **hidden pages**
* You want to capture specific pages
* Automatic page navigation isn't available
* You want complete control over which pages are captured

### Workflow

```text
Enter Power BI URL
        ↓
Validate URL
        ↓
Open Power BI report
        ↓
Wait for visuals
        ↓
Capture Page 1
        ↓
Manually navigate
        ↓
Capture Page 2
        ↓
Continue...
```

The script also performs an additional rendering process using scrolling and browser resize events. This helps when Power BI/custom visuals don't fully render after the initial waiting period.

---

# 🤖 Version 2 — Automatic Navigation

[View Automatic Version](PowerBI_Capture_Auto.py)

```text
powerbi_screenshot_auto.py
```

After building the manual version, I wanted to see if the page navigation itself could be automated.

Version 2 searches for the **Next Page** navigation and automatically moves through the report.

### Workflow

```text
Enter Power BI URL
        ↓
Validate URL
        ↓
Open Power BI report
        ↓
Wait for Power BI
        ↓
Capture Page
        ↓
Find Next Page
        ↓
Click Next Page
        ↓
Wait for transition
        ↓
Wait for visuals
        ↓
Check page changed
        ↓
Capture next page
        ↓
Repeat
```

### ⚠️ Important limitation

The automatic version depends on the **Next Page navigation being available and detectable in the public Power BI report**.

If the public report does not expose usable Next Page navigation, the automatic version cannot automatically move to the next page.

In that situation, use the **Manual Navigation Version**.

---

# 🆚 Manual vs Automatic

|                         | Manual Version | Automatic Version |
| ----------------------- | -------------- | ----------------- |
| Navigation              | Manual         | Automatic         |
| Hidden pages            | ✅ Useful       | ⚠️ Limited        |
| Specific page selection | ✅              | ⚠️                |
| Next Page required      | ❌              | ✅                 |
| Screenshot capture      | ✅              | ✅                 |
| Rendering handling      | ✅              | ✅                 |
| Page state detection    | —              | ✅                 |

### Simple rule

**Need more control? → Use Version 1**

**Next Page is available and you want automation? → Use Version 2**

---

# 🛠️ Requirements

### Python

Python 3.9+ recommended.

Check your Python installation:

```bash
python --version
```

### Install Playwright

```bash
pip install playwright
```

### Install Chromium

```bash
playwright install chromium
```

### Libraries used

The project mainly uses:

```text
Playwright
```

Python's built-in libraries:

```text
os
time
urllib.parse
```

do not require separate installation.

---

# 📥 Project Structure

```text
powerbi-screenshot-exporter/
│
├── README.md
│
├── powerbi_screenshot_manual.py
│
├── powerbi_screenshot_auto.py
│
└── requirements.txt
```

---

# 📦 requirements.txt

```text
playwright
```

Install using:

```bash
pip install -r requirements.txt
```

Then:

```bash
playwright install chromium
```

---

# 🚀 How to Use

## Version 1 — Manual

Run:

```bash
python powerbi_screenshot_manual.py
```

Enter your public Power BI report URL:

```text
https://app.powerbi.com/view?r=...
```

The script validates the URL before opening the report.

If an invalid URL is entered, it displays:

```text
============================================================
INVALID POWER BI URL
============================================================

Please enter a valid Public Power BI report URL.

Example:
https://app.powerbi.com/view?r=...
```

The script then asks you to enter the URL again.

Navigate to each report page manually and press Enter when the page is ready.

---

## Version 2 — Automatic

Run:

```bash
python powerbi_screenshot_auto.py
```

Enter the public Power BI report URL.

The script will automatically:

1. Open the report
2. Wait for Power BI
3. Prepare the visuals
4. Capture the current page
5. Find the Next Page button
6. Click Next Page
7. Wait for the transition
8. Check whether the page changed
9. Capture the next page
10. Continue until navigation stops

---

# 📸 Output

Screenshots are automatically saved as:

```text
Page_01.png
Page_02.png
Page_03.png
Page_04.png
```

For example:

```text
D:\PowerBI_Export\
│
├── Page_01.png
├── Page_02.png
├── Page_03.png
└── Page_04.png
```

The output location can be changed inside the Python script:

```python
OUTPUT_FOLDER = r"D:\PowerBI_Export"
```

---

# 🎨 Power BI / Custom Visual Rendering

One of the challenges I found while building this was that simply waiting for the Power BI page to load wasn't always enough.

Some custom visuals can still require additional time to render.

The scripts therefore perform an additional rendering sequence:

```text
Wait
 ↓
Scroll to top
 ↓
Trigger resize
 ↓
Scroll to bottom
 ↓
Scroll back to top
 ↓
Trigger resize again
 ↓
Wait
 ↓
Capture screenshot
```

This gives Power BI and custom visuals additional opportunities to recalculate their layout and render before the screenshot is captured.

---

# 🧠 Automatic Page Detection

Version 2 also checks whether the report actually changed after clicking **Next Page**.

It reads information from the Power BI page, including:

* Visible text
* ARIA labels
* SVG elements
* Canvas elements

The information is then used to compare the page before and after navigation.

The script also keeps track of previously visited page states to help prevent repeated navigation.

---

# ⚠️ Important Notes

### Public Power BI reports

The scripts are designed for **publicly accessible Power BI reports**.

URL validation checks whether the entered URL belongs to the Power BI domain, but it does not guarantee that the report itself is publicly accessible.

### Automatic navigation

Version 2 requires usable **Next Page** navigation in the public report.

If that isn't available, use Version 1.

### Rendering time

Some reports and custom visuals may require more time to load.

If necessary, increase the waiting time in the script.

---

# 💡 Why I Built This

This project started while I was **exploring Python**.

Instead of only practicing Python with small examples, I wanted to experiment with something connected to a real workflow I use.

That led to a simple question:

> **Can I automate Power BI screenshot capture using Python?**

I started with a manual version.

Once that worked, I started experimenting with automatic page navigation and built a second version.

So this project became a small example of how exploring a programming language can lead to solving a practical problem.

---

# 🚀 Future Ideas

Some improvements I may explore in the future:

* Better page detection
* More reliable navigation
* Configurable screenshot resolution
* Automatic page naming
* Better custom visual readiness detection
* More Power BI navigation scenarios
* GUI version
* Web-based version
* Cloud-based screenshot processing

---

## ⭐ Project

Built with:

**Python + Playwright + Power BI**

If you find the project useful, feel free to check out the code and experiment with it.

**Happy automating! 🚀**
