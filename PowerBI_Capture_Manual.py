
from playwright.sync_api import sync_playwright
import os
import time


# ============================================================
# SETTINGS
# ============================================================

OUTPUT_FOLDER = r"D:\PowerBI_Export"

WAIT_SECONDS = 15


# ============================================================
# ASK FOR POWER BI URL
# ============================================================

print("=" * 60)
print("POWER BI SCREENSHOT EXPORTER")
print("=" * 60)

print()

REPORT_URL = input(
    "Enter Power BI report URL: "
).strip()


if not REPORT_URL:

    print("No URL entered.")
    input("Press Enter to close...")
    raise SystemExit


# ============================================================
# ASK FOR NUMBER OF PAGES
# ============================================================

print()

while True:

    try:

        TOTAL_PAGES = int(
            input(
                "Enter number of report pages: "
            )
        )

        if TOTAL_PAGES > 0:
            break

        print(
            "Please enter a number greater than 0."
        )

    except ValueError:

        print(
            "Please enter a valid number."
        )


# ============================================================
# CREATE OUTPUT FOLDER
# ============================================================

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


print()

print(
    "Images will be saved here:"
)

print(
    OUTPUT_FOLDER
)


# ============================================================
# CLEAN PREVIOUS SCREENSHOTS
# ============================================================

print()

print(
    "Cleaning previous screenshots..."
)

for file in os.listdir(
    OUTPUT_FOLDER
):

    if file.lower().endswith(".png"):

        try:

            os.remove(
                os.path.join(
                    OUTPUT_FOLDER,
                    file
                )
            )

        except Exception:
            pass


# ============================================================
# START PLAYWRIGHT
# ============================================================

with sync_playwright() as p:

    # --------------------------------------------------------
    # Launch Chromium
    # --------------------------------------------------------

    browser = p.chromium.launch(

        headless=False,

        args=[

            "--disable-blink-features=AutomationControlled",

            "--enable-gpu",

            "--ignore-gpu-blocklist",

            "--enable-webgl",

            "--use-gl=desktop",

            "--disable-dev-shm-usage"
        ]
    )


    # --------------------------------------------------------
    # Browser context
    # --------------------------------------------------------

    context = browser.new_context(

        viewport={
            "width": 1920,
            "height": 1080
        },

        device_scale_factor=2
    )


    # --------------------------------------------------------
    # New page
    # --------------------------------------------------------

    page = context.new_page()


    # ========================================================
    # OPEN REPORT
    # ========================================================

    print()

    print(
        "Opening Power BI report..."
    )

    page.goto(

        REPORT_URL,

        wait_until="domcontentloaded",

        timeout=120000
    )


    # ========================================================
    # INITIAL WAIT
    # ========================================================

    print()

    print(
        f"Waiting {WAIT_SECONDS} seconds "
        f"for Power BI / ZoomCharts..."
    )

    time.sleep(
        WAIT_SECONDS
    )


    # ========================================================
    # PAGE-BY-PAGE SCREENSHOT
    # ========================================================

    for page_number in range(
        1,
        TOTAL_PAGES + 1
    ):

        print()
        print("=" * 60)

        print(
            f"PAGE {page_number} OF "
            f"{TOTAL_PAGES}"
        )

        print("=" * 60)


        # ----------------------------------------------------
        # Tell user to navigate manually
        # ----------------------------------------------------

        if page_number == 1:

            print()

            print(
                "Page 1 should be currently visible."
            )

        else:

            print()

            print(
                "Navigate to the NEXT report page "
                "in the browser."
            )

            print()

            input(
                "Press ENTER after the page is visible..."
            )


        # ----------------------------------------------------
        # Wait for visuals
        # ----------------------------------------------------

        print()

        print(
            f"Waiting {WAIT_SECONDS} seconds "
            f"for visuals..."
        )

        time.sleep(
            WAIT_SECONDS
        )


        # ----------------------------------------------------
        # Trigger Power BI rendering
        # ----------------------------------------------------

        try:

            page.evaluate("""
                window.scrollTo(0, 0);

                window.dispatchEvent(
                    new Event('resize')
                );
            """)

            time.sleep(2)


            page.evaluate("""
                window.scrollTo(
                    0,
                    document.body.scrollHeight
                );
            """)

            time.sleep(2)


            page.evaluate("""
                window.scrollTo(0, 0);
            """)

            time.sleep(2)


            page.evaluate("""
                window.dispatchEvent(
                    new Event('resize')
                );
            """)

            time.sleep(3)

        except Exception:
            pass


        # ----------------------------------------------------
        # Screenshot filename
        # ----------------------------------------------------

        screenshot_path = os.path.join(

            OUTPUT_FOLDER,

            f"Page_{page_number:02d}.png"
        )


        # ----------------------------------------------------
        # Take screenshot
        # ----------------------------------------------------

        print()

        print(
            "Saving:"
        )

        print(
            screenshot_path
        )


        page.screenshot(

            path=screenshot_path,

            full_page=False,

            animations="disabled"
        )


        print()

        print(
            "✓ Screenshot saved."
        )


    # ========================================================
    # COMPLETE
    # ========================================================

    print()
    print("=" * 60)
    print("EXPORT COMPLETE")
    print("=" * 60)

    print()

    print(
        f"Total pages captured: "
        f"{TOTAL_PAGES}"
    )

    print()

    print(
        "Files saved:"
    )


    for page_number in range(
        1,
        TOTAL_PAGES + 1
    ):

        print(
            f"✓ Page_{page_number:02d}.png"
        )


    print()

    print(
        f"Location: {OUTPUT_FOLDER}"
    )


    # ========================================================
    # KEEP BROWSER OPEN
    # ========================================================

    input(
        "\nPress Enter to close browser..."
    )


    browser.close()