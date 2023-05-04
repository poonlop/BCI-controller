import cortex
from cortex import Cortex
import socket


# init bci connection with cortex
bci_client_id = "vM1pkIlN5DjGKwgtQKto49fG50CnS5yKgrp1g2Ve"
bci_client_secret = "rPbxdGZs2Amh1YRSNeKRabNaaN0rJMQLwE2ZLGSQBMk5cT6fY1VZtL3cGdzSXfHKqm04eGXccBIBLKLpwjwTHTSolu9hUWhPn7wSfL0r6mwOXjtTyhzEEdz6MQ0sOiVD"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "172.20.10.8"  # replace with hotspot IP address

# set the port number
port = 58707


# send command function
def send_command(s: socket, command):
    s.sendall(command.encode())
    print(f"Sent command: {command}")
    response = s.recv(1024).decode()
    print(response)


class StreamCommand:
    def __init__(self, app_client_id, app_client_secret, **kwargs):
        self.c = Cortex(app_client_id, app_client_secret, debug_mode=False, **kwargs)
        self.c.bind(create_session_done=self.on_create_session_done)
        self.c.bind(query_profile_done=self.on_query_profile_done)
        self.c.bind(load_unload_profile_done=self.on_load_unload_profile_done)
        self.c.bind(save_profile_done=self.on_save_profile_done)
        self.c.bind(new_com_data=self.on_new_com_data)
        self.c.bind(get_mc_active_action_done=self.on_get_mc_active_action_done)
        self.c.bind(mc_action_sensitivity_done=self.on_mc_action_sensitivity_done)
        self.c.bind(inform_error=self.on_inform_error)

    def start(self, profile_name, headsetId=""):
        if profile_name == "":
            raise ValueError("Empty profile_name. The profile_name cannot be empty.")

        self.profile_name = profile_name
        self.c.set_wanted_profile(profile_name)

        if headsetId != "":
            self.c.set_wanted_headset(headsetId)
        # print(':P')
        self.c.open()
        # print('hi')

    def load_profile(self, profile_name):
        self.c.setup_profile(profile_name, "load")

    def unload_profile(self, profile_name):
        self.c.setup_profile(profile_name, "unload")

    def save_profile(self, profile_name):
        self.c.setup_profile(profile_name, "save")

    def subscribe_data(self, streams):
        self.c.sub_request(streams)

    def get_active_action(self, profile_name):
        self.c.get_mental_command_active_action(profile_name)

    def get_sensitivity(self, profile_name):
        self.c.get_mental_command_action_sensitivity(profile_name)

    def set_sensitivity(self, profile_name, values):
        self.c.set_mental_command_action_sensitivity(profile_name, values)

    # set default value for filtered command

    is_moving = False
    avg_power = 0.5280443742514973
    action_con = 0

    def filter_command(self, action, power):
        # type of action available
        action_type = ["push", "right", "left"]

        # send command part

        print("is_moving: ", self.is_moving)
        # when the car is not moving
        if not self.is_moving:
            # if action have morepower than the avg power, action count +1
            if action in action_type and power >= self.avg_power:
                self.action_con += 1
            print("action_con: ", self.action_con)

            # if action changed from previous action or power less than avg power, reset action
            if action == "neutral" or power < self.avg_power:
                self.action_con = 0

            # if repeat consecutive action happens more than criteria, send "action"
            if self.action_con >= 3:
                self.is_moving = True
                print("set is_moving to True")
                self.action_con = 0
                print("reset action_con = 0")
                send_command(s, action)
                print("send command done")

        if self.is_moving:
            if action == "neutral" or power < self.avg_power:
                send_command(s, "stop")
                self.is_moving = False

    # callbacks functions
    def on_create_session_done(self, *args, **kwargs):
        print("on_create_session_done")
        self.c.query_profile()

    def on_query_profile_done(self, *args, **kwargs):
        print("on_query_profile_done")
        self.profile_lists = kwargs.get("data")
        if self.profile_name in self.profile_lists:
            # the profile is existed
            self.c.get_current_profile()
        else:
            # create profile
            self.c.setup_profile(self.profile_name, "create")

    def on_load_unload_profile_done(self, *args, **kwargs):
        is_loaded = kwargs.get("isLoaded")
        print("on_load_unload_profile_done: " + str(is_loaded))

        if is_loaded == True:
            # get active action
            self.get_active_action(self.profile_name)
        else:
            print("The profile " + self.profile_name + " is unloaded")
            self.profile_name = ""

    def on_save_profile_done(self, *args, **kwargs):
        print("Save profile " + self.profile_name + " successfully")
        # subscribe mental command data
        stream = ["com"]
        self.c.sub_request(stream)

    def on_new_com_data(self, *args, **kwargs):
        """
        To handle mental command data emitted from Cortex

        Returns
        -------
        data: dictionary
             the format such as {'action': 'neutral', 'power': 0.0, 'time': 1590736942.8479}
        """
        data = kwargs.get("data")
        print("mc data: {}".format(data))
        action = data["action"]
        power = data["power"]
        time = data["time"]
        self.filter_command(action, power)

    def on_get_mc_active_action_done(self, *args, **kwargs):
        data = kwargs.get("data")
        print("on_get_mc_active_action_done: {}".format(data))
        self.get_sensitivity(self.profile_name)

    def on_mc_action_sensitivity_done(self, *args, **kwargs):
        data = kwargs.get("data")
        print("on_mc_action_sensitivity_done: {}".format(data))
        if isinstance(data, list):
            # get sensivity
            new_values = [7, 7, 5, 5]
            self.set_sensitivity(self.profile_name, new_values)
        else:
            # set sensitivity done -> save profile
            self.save_profile(self.profile_name)

    def on_inform_error(self, *args, **kwargs):
        error_data = kwargs.get("error_data")
        error_code = error_data["code"]
        error_message = error_data["message"]

        print(error_data)

        if error_code == cortex.ERR_PROFILE_ACCESS_DENIED:
            # disconnect headset for next use
            print(
                "Get error "
                + error_message
                + ". Disconnect headset to fix this issue for next use."
            )
            self.c.disconnect_headset()


# -----------------------------------------------------------
#
# GETTING STARTED
#   - Please reference to https://emotiv.gitbook.io/cortex-api/ first.
#   - Connect your headset with dongle or bluetooth. You can see the headset via Emotiv Launcher
#   - Please make sure the your_app_client_id and your_app_client_secret are set before starting running.
#   - The function on_create_session_done,  on_query_profile_done, on_load_unload_profile_done will help
#          handle create and load an profile automatically . So you should not modify them
#   - After the profile is loaded. We test with some advanced BCI api such as: mentalCommandActiveAction, mentalCommandActionSensitivity..
#      But you can subscribe 'com' data to get live mental command data after the profile is loaded
# RESULT
#    you can run live mode with the trained profile. the data as below:
#    {'action': 'push', 'power': 0.85, 'time': 1647525819.0223}
#    {'action': 'pull', 'power': 0.55, 'time': 1647525819.1473}
#
# -----------------------------------------------------------


def main():
    # Please fill your application clientId and clientSecret before running script
    your_app_client_id = "vM1pkIlN5DjGKwgtQKto49fG50CnS5yKgrp1g2Ve"
    your_app_client_secret = "rPbxdGZs2Amh1YRSNeKRabNaaN0rJMQLwE2ZLGSQBMk5cT6fY1VZtL3cGdzSXfHKqm04eGXccBIBLKLpwjwTHTSolu9hUWhPn7wSfL0r6mwOXjtTyhzEEdz6MQ0sOiVD"

    # connect to the ESP
    s.connect((host, port))
    print("successfully connected to ESP")

    # Init live advance
    print("start live_advance")
    l = StreamCommand(your_app_client_id, your_app_client_secret)

    trained_profile_name = "Poon"  # Please set a trained profile name here
    l.start(trained_profile_name)


if __name__ == "__main__":
    main()

# -----------------------------------------------------------
