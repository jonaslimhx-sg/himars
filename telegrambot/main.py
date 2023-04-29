import os
import telebot
from dotenv import load_dotenv
import time

import griddle_utils
import fmsn_utils
import conversion_utils
import constants

load_dotenv()

GRIDS_DELIMITER = constants.GRIDS_DELIMITER
E_N_DELIMITER = constants.E_N_DELIMITER
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)


###############
## Start Up ##
###############
@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        constants.start_message
    )

@bot.message_handler(commands=["fmsn"])
def configurations(message):
    bot.reply_to(
        message,
        constants.guide
    )

###############
## Griddling ##
###############
@bot.message_handler(commands=["set_griddle"])
def receive_code(message):
    coordinates = bot.reply_to(
        message,
        constants.set_griddle
    )
    bot.register_next_step_handler(coordinates, set_griddle)

def set_griddle(message):
    time.sleep(2)

    try:
        _, _, _, _ = griddle_utils.get_griddle_contents(message.text)

        with open("griddle_table.txt", "w") as f:
            f.write(message.text)
            f.flush()

        bot.reply_to(message, "Griddle Table Set") 

    except Exception as e:
        bot.reply_to(message, f"[ERROR]\n{e}")

@bot.message_handler(commands=["get_griddle"])
def get_griddle(message):
    time.sleep(2)

    if not os.path.exists("griddle_table.txt"):
        bot.reply_to(message, "[ERROR]\n No Griddle Table has been set")
    else:
        bot.reply_to(message, open("griddle_table.txt", "r").read())

@bot.message_handler(commands=["griddle"]) 
def receive_code(message):
    coordinates = bot.reply_to(
        message, 
        constants.griddle
    )
    bot.register_next_step_handler(coordinates, griddle)

def griddle(message):
    time.sleep(2)

    try:

        if not os.path.exists("griddle_table.txt"):
            bot.reply_to(message, "[ERROR]\n No Griddle Table has been set")
        else:

            grids = message.text.split(GRIDS_DELIMITER)
            results = ""
            for grid in grids:

                easting, northing = grid.split(E_N_DELIMITER)
                assert (len(easting)==5) and (len(northing)==5), "Easting or Northing is not 5 digit."

                # Handle Easting
                results += griddle_utils.griddle(easting[:2], mode="easting", first_griddle=True)
                for num_str in easting[2:]:
                    results += griddle_utils.griddle(num_str, mode="easting")

                results += E_N_DELIMITER

                # Handle Northing
                results += griddle_utils.griddle(northing[:2], mode="northing", first_griddle=True)
                for num_str in northing[2:]:
                    results += griddle_utils.griddle(num_str, mode="northing")
                
                results += GRIDS_DELIMITER

            bot.reply_to(message, results)

    except Exception as e:
        bot.reply_to(message, "[Error] \n{}".format(e))

@bot.message_handler(commands=["degriddle"])
def receive_code(message):
    coordinates = bot.reply_to(
        message, 
        constants.degriddle
    )
    bot.register_next_step_handler(coordinates, degriddle)

def degriddle(message):
    time.sleep(2)
    try:
        grids: list =  message.text.split(GRIDS_DELIMITER)

        results = ""
        for grid in grids:

            easting, northing = grid.split(E_N_DELIMITER)
            assert (len(easting)==4) and (len(northing)==4), "One of the grids ddoes not have 4 alphabets."

            # Handle Easting
            for i,alphabet in enumerate(easting.upper()):
                result = griddle_utils.degriddle(alphabet, mode="easting")
                results += str(result) if i == 0 else str(result)[-1]

            results += E_N_DELIMITER

            # Handle Northing
            for i,alphabet in enumerate(northing.upper()):
                result = griddle_utils.degriddle(alphabet, mode="northing")
                results += str(result) if i == 0 else str(result)[-1]
            
            results += GRIDS_DELIMITER

        bot.reply_to(message, results)

    except Exception as e:
        bot.reply_to(message, "[Error]\n{}".format(e))


################
## RSO UTM Conversion ##
################
@bot.message_handler(commands=["rso_to_utm"])
def receive_code(message):
    grids = bot.reply_to(message,
    constants.rso_to_utm
    )
    bot.register_next_step_handler(grids, rso_to_utm)

def rso_to_utm(message):
    time.sleep(2)

    try:
        grids = message.text.split(GRIDS_DELIMITER)
        results = ""

        for grid in grids:

            easting, northing = conversion_utils.conversion(grid, mode="rso_to_utm")
            results += f"{easting} {northing}\n"
        
        bot.reply_to(message, results)
    
    except Exception as e:
        bot.reply_to(message, f"[Error]\n{e}")

@bot.message_handler(commands=["utm_to_rso"])
def receive_code(message):
    grids = bot.reply_to(message,
    constants.utm_to_rso
    )
    bot.register_next_step_handler(grids, utm_to_rso)

def utm_to_rso(message):
    time.sleep(2)
    try:
        grids = message.text.split(GRIDS_DELIMITER)
        results = ""

        for grid in grids:
            
            easting, northing = conversion_utils.conversion(grid, mode="utm_to_rso")
            results += f"{easting} {northing}\n"

        bot.reply_to(message, results)
    
    except Exception as e:
        bot.reply_to(message, "[Error]\n{}".format(e))

#################
## SETUP ##
#################
@bot.message_handler(commands=["get_fp"])
def get_firing_point(message):
    time.sleep(2)

    if not os.path.exists("firing_point.txt"):
        bot.reply_to(message, "[ERROR]\nNo Firing Point has been set")
    else:
        bot.reply_to(message, open("firing_point.txt", "r").read())

@bot.message_handler(commands=["set_utm_fp"])
def set_firing_point(message):
    time.sleep(1)

    try:
        temp:list = message.text.split(" ")
        assert len(temp) == 3, "Invalid Firing Point"
        _, easting, northing = temp
        assert (len(easting)==6) and (len(northing)==6), "Easting and Northing is not 6 digits."
        
        with open("firing_point.txt", "w") as f:
            f.write(f"{easting} {northing}")
            f.flush()

        bot.reply_to(message, f"FP set as {easting} {northing}")
            
    except Exception as e:
        bot.reply_to(message, f"[ERROR]\n{e}")

@bot.message_handler(commands=["get_dof"])
def get_dof(message):
    time.sleep(2)

    if not os.path.exists("firing_point.txt"):
        bot.reply_to(message, "[ERROR]\nNo DOF has been set")
    else:
        bot.reply_to(message, open("dof.txt","r").read())

@bot.message_handler(commands=["set_dof"])
def set_dof(message):
    time.sleep(1)

    try:
        temp: list = message.text.split(" ")
        assert len(temp) == 2, "No DOF has been entered"
        _, dof = temp

        with open("dof.txt", "w") as f:
            f.write(dof)
            f.flush()
        bot.reply_to(message, f"DOF set as {dof}")

    except Exception as e:
        bot.reply_to(message, f"[ERROR]\n{e}")

#################
## FMSN CHECKS ##
#################

@bot.message_handler(commands=["fmsn_fdo"])
def receive_code(message):
    response = bot.reply_to(
        message,
        constants.fmsn_fdo
    )
    bot.register_next_step_handler(response, utm_firing_check)

def utm_firing_check(message):
    time.sleep(2)
    results = ""

    try:
        # Find out number of TGs
        grids = message.text.split(GRIDS_DELIMITER)
        for grid in grids:
            results += f"*[ {grid} ]*\n" # Use each grid as header
            easting, northing, ammo, traj = grid.split(E_N_DELIMITER)
            
            assert (len(easting)==6) and (len(northing)==6), "Easting and Northing is not 6 digits."
            
            # range_check
            response, range, dof = fmsn_utils.range_check(int(easting),int(northing), ammo, traj)
            results += f"R: {range}km\nθ: {dof}mils\n"
            results += f"{response}\n"

            # overhead_firing check
            response = fmsn_utils.overhead_firing_check(dof)
            results += f"{response}\n\n"
        
        bot.reply_to(message, results, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"[ERROR]\n{e}")

@bot.message_handler(commands=["fmsn_fo"])
def receive_code(message):
    response = bot.reply_to(
        message,
        constants.fmsn_fo
    )
    bot.register_next_step_handler(response, rso_firing_check)
    
def rso_firing_check(message):
    time.sleep(2)
    results = ""

    try:
        # Find out number of TGs
        grids = message.text.split(GRIDS_DELIMITER)
        for grid in grids:
            results += f"*[ {grid} ]*\n" # Use each grid as header
            easting, northing, ammo, traj = grid.split(E_N_DELIMITER)
            
            assert (len(easting)==6) and (len(northing)), "Easting and Northing is not 6 digits."
            
            # Convert RSO to UTM
            easting, northing = conversion_utils.conversion(grid, mode="rso_to_utm")
            results += f"UTM: {easting} {northing}\n"

            # range_check
            response, range, dof = fmsn_utils.range_check(easting,northing, ammo, traj)
            results += f"R: {range}km\nθ: {dof}mils\n"
            results += f"{response}\n"

            # overhead_firing check
            response = fmsn_utils.overhead_firing_check(dof)
            results += f"{response}\n\n"
        
        bot.reply_to(message, results, parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, f"[ERROR]\n{e}")


bot.delete_my_commands(scope=None, language_code=None)
bot.set_my_commands(
    commands = [
        telebot.types.BotCommand("/fmsn_fdo", "Fmsn w/ UTM Target Grids"),
        telebot.types.BotCommand("/fmsn_fo", "Fmsn w/ RSO Target Grids"),
        telebot.types.BotCommand("/rso_to_utm", "Convert RSO to UTM"),
        telebot.types.BotCommand("/utm_to_rso", "Convert UTM to RSO"),
        telebot.types.BotCommand("/griddle", "Convert Numbers to Alphabets"),
        telebot.types.BotCommand("/degriddle", "Convert Alphbets to Numbers"),
        telebot.types.BotCommand("/set_utm_fp", "Set UTM Firing Point"),
        telebot.types.BotCommand("/set_dof", "Set DOF"),
        telebot.types.BotCommand("/set_griddle", "Set Griddle Table"),
        telebot.types.BotCommand("/get_fp", "Get UTM Firing Point"),
        telebot.types.BotCommand("/get_dof", "Get DOF"),
        telebot.types.BotCommand("/get_griddle", "Get Griddle Table")
    ]
)

# bot.infinity_polling(restart_on_change=True, interval=1)
bot.polling(interval=3)
