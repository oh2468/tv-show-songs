from settings import *
from tunefind_scraper import TunefindScraper
from database_handler import DBHandler
import os


def print_db_results(show, results):
    columns, rows = results
    print(DB_RESULT_MSG.format(show=show))
    print(columns)
    for row in sorted(rows):
        print(row)


def print_scrape_results(results):
    success, msg = results
    print(SUCCESS_MSG if success else ERROR_MSG)
    print(msg)


def get_show_name(required):
    if required:
        while not (show_name := input("Enter a show name: ")):
            pass
        return show_name
    else:
        return input(f"Enter a show name (leave blank for all): ")


def get_show_season():
    try:
        return int(input("Enter a season number: "))
    except:
        print(INVALID_NUM_MSG)
        return get_show_season()


def should_update_show_name():
    while (choice := input("Change show? (y/n): ")) != "y" and choice != "n":
        pass
    return choice == "y"


def update_scraper_if_needed(scraper):
    if not scraper or should_update_show_name():
        scraper = TunefindScraper(get_show_name(True))
    return scraper


def call_scraper_function(func, season_needed):
    res = func(get_show_season() if season_needed else None)
    print_scrape_results(res)


def call_dbhandler_function(func, required):
    show_name = get_show_name(required)
    res = func(show_name)
    print_db_results(show_name, res)


def call_delete_function(func, show_needed, season_needed, confirmation_msg):
    name = get_show_name(show_needed) if show_needed or season_needed else None
    season = get_show_season() if season_needed else None

    print(WARNING_MSG)
    while (ans := input(f"{confirmation_msg.format(show=name, season=season)} (y/n): ")) != "y":
        if ans == "n":
            print(ABORT_DELETE_MSG)
            return True

    res = func(name, season) if season_needed else (func(name) if show_needed else func())
    
    print(DELETE_SUCCESS_MSG if res else DELETE_ERROR_MSG)


if __name__ == "__main__":
    print(WELCOME_MSG)

    scraper = None
    dbHandler = DBHandler()

    print(APP_OPTIONS)
    while (choice := input("Choose an option: ")) != "0":
        try:
            ch_val = int(choice)
        except ValueError:
            pass
        else:
            if -1 < ch_val and ch_val < 5 and ch_val != 3:
                scraper = update_scraper_if_needed(scraper)

        match choice:
            case "1":
                call_scraper_function(scraper.scrape_show, False)
            case "2":
                call_scraper_function(scraper.scrape_show, True)
            case "3":
                print(NOT_IMPLEMENTED_MSG)
            case "4":
                call_scraper_function(scraper.update_spotify_links, True)
            case "5":
                call_dbhandler_function(dbHandler.get_shows, False)
            case "6":
                call_dbhandler_function(dbHandler.get_seasons, False)
            case "7":
                call_dbhandler_function(dbHandler.get_episodes, False)
            case "8":
                call_dbhandler_function(dbHandler.get_songs, False)
            case "9":
                print(TOTAL_COUNT_SONGS.format(count=dbHandler.get_song_count()))
            case "10":
                show_name = get_show_name(True)
                print(TOTAL_COUNT_SHOW_SONGS.format(show_name=show_name, count=dbHandler.get_song_count(show_name)))
            case "11":
                call_delete_function(dbHandler.delete_show, True, False, CONFIRM_DELETE_SHOW)
            case "12":
                call_delete_function(dbHandler.delete_season, True, True, CONFIRM_DELETE_SEASON)
            case "13":
                aborted = call_delete_function(dbHandler.delete_everything, False, False, CONFIRM_DELETE_EVERTHING)
                if not aborted:
                    print(EVERYTHING_DELETED)
                    break
            case "14":
                dbHandler.export_songs_to_csv()
                pass
            case "15":
                # export db to script
                print("Not yet implemented, coming soon (or never, undecided)")
            case "16":
                # export db to pickle
                print("Not yet implemented, coming soon (or never, undecided)")
            case "17":
                # export db to json
                print("Not yet implemented, coming soon (or never, undecided)")
            case "cl":
                os.system("cls" if os.name=="nt" else "clear")
            case _:
                print(f"INVALID OPTION ENTERED: {choice}")
        
        print(f"  {'-_-*' * 20}\n{APP_OPTIONS}\n")

    print(GOODBYE_MSG)

