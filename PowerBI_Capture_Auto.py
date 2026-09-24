from playwright.sync_api import sync_playwright
from urllib.parse import urlparse
import time
import os


# ============================================================
# POWER BI URL VALIDATION
# ============================================================

def is_valid_powerbi_url(url):
    """
    Validate that the entered URL belongs to Power BI.

    This checks the URL format and Power BI domain.
    It does NOT verify whether the report is actually public.
    """

    try:

        parsed = urlparse(url)

        # Must use HTTP or HTTPS
        if parsed.scheme not in ["http", "https"]:
            return False

        hostname = (parsed.hostname or "").lower()

        # Main Power BI domain
        if hostname == "app.powerbi.com":
            return True

        # Other Power BI subdomains
        if hostname.endswith(".powerbi.com"):
            return True

        return False

    except Exception:

        return False


# ============================================================
# INVALID URL MESSAGE
# ============================================================

def show_invalid_url_message():

    print()
    print("=" * 60)
    print("INVALID POWER BI URL")
    print("=" * 60)
    print()

    print("Please enter a valid Public Power BI report URL.")

    print()

    print("Example:")
    print("https://app.powerbi.com/view?r=...")

    print()


# ============================================================
# ASK FOR POWER BI URL
# ============================================================

print("=" * 60)
print("POWER BI SCREENSHOT EXPORTER")
print("=" * 60)
print()


while True:

    POWER_BI_URL = input(
        "Paste Power BI report URL: "
    ).strip()

    # --------------------------------------------------------
    # EMPTY URL
    # --------------------------------------------------------

    if not POWER_BI_URL:

        show_invalid_url_message()

        continue


    # --------------------------------------------------------
    # INVALID POWER BI URL
    # --------------------------------------------------------

    if not is_valid_powerbi_url(POWER_BI_URL):

        show_invalid_url_message()

        continue


    # --------------------------------------------------------
    # VALID URL
    # --------------------------------------------------------

    print()
    print("✓ Valid Power BI URL.")

    break


# ============================================================
# OUTPUT FOLDER
# ============================================================

OUTPUT_FOLDER = r"D:\PowerBI_Export"


os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


print()
print("Images will be saved here:")
print(OUTPUT_FOLDER)


# ============================================================
# WAIT FOR POWER BI VISUALS
# ============================================================

def wait_for_visuals(page, page_number):

    print("\n" + "-" * 60)

    print(
        f"Preparing Page {page_number}"
    )

    print("-" * 60)


    # --------------------------------------------------------
    # INITIAL WAIT
    # --------------------------------------------------------

    print(
        "Waiting 15 seconds for Power BI Visuals"
    )

    time.sleep(15)


    # --------------------------------------------------------
    # TRIGGER RENDERING
    # --------------------------------------------------------

    try:

        # Scroll to top + resize
        page.evaluate("""
            () => {

                window.scrollTo(0, 0);

                window.dispatchEvent(
                    new Event('resize')
                );

            }
        """)

        time.sleep(2)


        # Scroll to bottom
        page.evaluate("""
            () => {

                window.scrollTo(
                    0,
                    document.body.scrollHeight
                );

            }
        """)

        time.sleep(2)


        # Scroll back to top
        page.evaluate("""
            () => {

                window.scrollTo(0, 0);

            }
        """)

        time.sleep(2)


        # Trigger resize again
        page.evaluate("""
            () => {

                window.dispatchEvent(
                    new Event('resize')
                );

            }
        """)

        time.sleep(3)


    except Exception as e:

        print(
            "Rendering warning:",
            e
        )


    print(
        f"Page {page_number} ready."
    )


# ============================================================
# GET REPORT STATE
# ============================================================

def get_report_state(page):

    try:

        return page.evaluate("""
            () => {

                // ============================================
                // BODY TEXT
                // ============================================

                const bodyText =
                    document.body.innerText || "";


                // ============================================
                // ARIA LABELS
                // ============================================

                const ariaElements =
                    Array.from(
                        document.querySelectorAll(
                            '[aria-label]'
                        )
                    )
                    .map(
                        el =>
                            el.getAttribute(
                                'aria-label'
                            )
                    )
                    .filter(Boolean)
                    .join('|');


                // ============================================
                // SVG COUNT
                // ============================================

                const svgCount =
                    document.querySelectorAll(
                        'svg'
                    ).length;


                // ============================================
                // CANVAS COUNT
                // ============================================

                const canvasCount =
                    document.querySelectorAll(
                        'canvas'
                    ).length;


                // ============================================
                // RETURN STATE
                // ============================================

                return (

                    bodyText.substring(
                        0,
                        15000
                    )

                    + "||ARIA||"

                    + ariaElements

                    + "||SVG||"

                    + svgCount

                    + "||CANVAS||"

                    + canvasCount

                );

            }
        """)

    except Exception:

        return ""


# ============================================================
# START PLAYWRIGHT
# ============================================================

with sync_playwright() as p:

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


    # ========================================================
    # BROWSER PAGE
    # ========================================================

    page = browser.new_page(

        viewport={
            "width": 1920,
            "height": 1080
        },

        device_scale_factor=2

    )


    # ========================================================
    # OPEN POWER BI
    # ========================================================

    print(
        "\nOpening Power BI report..."
    )


    try:

        page.goto(

            POWER_BI_URL,

            wait_until="domcontentloaded",

            timeout=120000

        )

    except Exception as e:

        print()
        print("=" * 60)
        print("UNABLE TO OPEN POWER BI REPORT")
        print("=" * 60)
        print()

        print(
            "The Power BI report could not be opened."
        )

        print()

        print(
            "Please make sure the report is publicly accessible."
        )

        print()

        print("Example:")
        print("https://app.powerbi.com/view?r=...")

        print()

        print("Browser error:")
        print(e)

        input(
            "\nPress Enter to close..."
        )

        browser.close()

        raise SystemExit


    # ========================================================
    # INITIAL LOAD
    # ========================================================

    print(
        "\nWaiting 15 seconds for Power BI..."
    )

    time.sleep(15)


    # ========================================================
    # PAGE COUNTER
    # ========================================================

    page_number = 1


    # ========================================================
    # VISITED PAGE STATES
    # ========================================================

    visited_states = set()


    # ========================================================
    # GET INITIAL PAGE STATE
    # ========================================================

    initial_state = get_report_state(page)


    if initial_state:

        visited_states.add(
            initial_state
        )


    # ========================================================
    # MAIN LOOP
    # ========================================================

    while True:

        print("\n")

        print("=" * 60)

        print(
            f"PROCESSING PAGE {page_number}"
        )

        print("=" * 60)


        # ====================================================
        # WAIT FOR VISUALS
        # ====================================================

        wait_for_visuals(

            page,

            page_number

        )


        # ====================================================
        # TAKE SCREENSHOT
        # ====================================================

        file_name = (

            f"Page_{page_number:02d}.png"

        )


        screenshot_path = os.path.join(

            OUTPUT_FOLDER,

            file_name

        )


        print(
            "\nTaking screenshot..."
        )


        try:

            page.screenshot(

                path=screenshot_path,

                full_page=False,

                animations="disabled"

            )

            print(
                "\n✓ Screenshot saved:"
            )

            print(
                screenshot_path
            )

        except Exception as e:

            print(
                "\n✗ Screenshot failed."
            )

            print(e)

            break


        # ====================================================
        # GET CURRENT PAGE STATE
        # ====================================================

        old_state = get_report_state(page)


        # ====================================================
        # FIND NEXT PAGE
        # ====================================================

        print(
            "\nSearching for Next Page..."
        )


        next_button = page.locator(

            '[aria-label="Next Page"]'

        )


        count = next_button.count()


        print(

            "Next Page buttons found:",

            count

        )


        # ====================================================
        # NO NEXT PAGE BUTTON
        # ====================================================

        if count == 0:

            print()

            print(
                "No Next Page button found."
            )

            print(
                "Reached final page."
            )

            break


        # Use the last matching button
        button = next_button.last


        # ====================================================
        # CHECK NEXT PAGE VISIBILITY
        # ====================================================

        try:

            if not button.is_visible():

                print()

                print(
                    "Next Page is not visible."
                )

                print(
                    "Reached final page."
                )

                break

        except Exception as e:

            print()

            print(
                "Unable to check Next Page visibility."
            )

            print(e)

            break


        # ====================================================
        # CHECK NEXT PAGE DISABLED
        # ====================================================

        try:

            if button.is_disabled():

                print()

                print(
                    "Next Page is disabled."
                )

                print(
                    "Reached final page."
                )

                break

        except Exception:

            # Some Power BI elements may not expose
            # disabled state. Continue if unavailable.

            pass


        # ====================================================
        # CLICK NEXT PAGE
        # ====================================================

        print()

        print(
            "Clicking Next Page..."
        )


        try:

            button.click(

                force=True

            )

        except Exception as e:

            print()

            print(
                "Could not click Next Page:"
            )

            print(e)

            break


        # ====================================================
        # WAIT FOR PAGE TRANSITION
        # ====================================================

        print()

        print(
            "Waiting 5 seconds for "
            "Power BI page transition..."
        )

        time.sleep(5)


        # ====================================================
        # WAIT FOR NEXT PAGE VISUALS
        # ====================================================

        next_page_number = page_number + 1


        wait_for_visuals(

            page,

            next_page_number

        )


        # ====================================================
        # GET NEW PAGE STATE
        # ====================================================

        print()

        print(
            "Checking whether the report page changed..."
        )


        new_state = get_report_state(page)


        # ====================================================
        # PAGE STATE EMPTY
        # ====================================================

        if not new_state:

            print()

            print(
                "Unable to read the new page state."
            )

            print(
                "Stopping screenshot process."
            )

            break


        # ====================================================
        # PAGE DID NOT CHANGE
        # ====================================================

        if (

            old_state

            and old_state == new_state

        ):

            print()

            print("=" * 60)

            print(
                "PAGE DID NOT CHANGE"
            )

            print("=" * 60)

            print()

            print(
                "The report remained on the same page."
            )

            print(
                "Stopping screenshot process."
            )

            break


        # ====================================================
        # PREVIOUS PAGE DETECTED
        # ====================================================

        if new_state in visited_states:

            print()

            print("=" * 60)

            print(
                "PREVIOUS PAGE DETECTED"
            )

            print("=" * 60)

            print()

            print(
                "The report navigated to a page "
                "that was already captured."
            )

            print(
                "Stopping screenshot process."
            )

            break


        # ====================================================
        # NEW PAGE DETECTED
        # ====================================================

        print()

        print(
            "✓ Page changed successfully."
        )


        # Add new state to visited pages
        visited_states.add(

            new_state

        )


        # Move to next page number
        page_number += 1


    # ========================================================
    # FINAL FILE CHECK
    # ========================================================

    print("\n")

    print("=" * 60)

    print("FILES CREATED")

    print("=" * 60)


    image_files = [

        file

        for file in os.listdir(

            OUTPUT_FOLDER

        )

        if file.lower().endswith(

            (".png", ".jpg", ".jpeg")

        )

    ]


    image_files.sort()


    for file in image_files:

        print(

            os.path.join(

                OUTPUT_FOLDER,

                file

            )

        )


    print()

    print(
        "Total pages captured:",
        len(image_files)
    )


    # ========================================================
    # OPEN OUTPUT FOLDER
    # ========================================================

    try:

        os.startfile(

            OUTPUT_FOLDER

        )

    except Exception as e:

        print()

        print(
            "Could not open output folder:"
        )

        print(e)


    # ========================================================
    # KEEP BROWSER OPEN
    # ========================================================

    input(

        "\nPress Enter to close browser..."

    )


    # ========================================================
    # CLOSE BROWSER
    # ========================================================

    browser.close()