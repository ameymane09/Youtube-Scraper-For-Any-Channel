import time
from scraper_basic import scraper_basic
from scraper_advanced import scraper_advanced
from shorts_scraper import shorts_scraper


if __name__ == '__main__':
    shorts_channels = [("https://www.youtube.com/@VarunMayya/shorts", "varun_mayya"),
                       ("https://www.youtube.com/@AbhiandNiyu/shorts", "abhi_and_niyu"),
                       ("https://www.youtube.com/@pranjalkamra/shorts", "pranjal_kamra"),
                       ("https://www.youtube.com/@_FinologyLegal/shorts", "priya_jain"),
                       ("https://www.youtube.com/@LabourLawAdvisor/shorts", "LLA"),
                       ("https://www.youtube.com/@NitishRajput/shorts", "nitish_rajput"),
                       ("https://www.youtube.com/@XYAxisEducation/shorts", "xy_axis_edu"),
                       ("https://www.youtube.com/@conveybyfinnovationz/shorts", "finnovationZ"),
                       ("https://www.youtube.com/@sochbymm/shorts", "soch")]

    loop_start = time.time()

    start = time.time()

    # Put the link of the videos page of the channel
    # scraper_basic("https://www.youtube.com/@sochbymm/videos")
    scraper_advanced("https://www.youtube.com/@sochbymm/videos")
    # shorts_scraper(shorts_channels[8][0], shorts_channels[8][1])

    end = time.time()
    # print(f"\n\nTotal time taken to scrape {channel[1]}'s channel: {round(end - start, 2)}s")

    loop_end = time.time()
    print(f"\n\nTotal time for the program to execute: {round(loop_end - loop_start, 2)}s")
