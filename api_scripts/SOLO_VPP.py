#!/usr/bin/env python3
#
# Copyright (c) 2019-2021 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import time
from environs import Env
import lgsvl
import requests

env = Env()

url = 'http://localhost/api/v1/clusters/start/apiOnly'
response = requests.get(url)

time.sleep(1)

#Vehicle Configs
VPP = '03efd1b6-0471-4e90-9372-e7e2ca1b4c25'
MultiCar1 = '30702b8f-8b8c-4860-b5ea-fcc27d8a01c0'
MultiCar2 = '99f0c685-1137-459c-b841-9c1041f18ca3'

#Maps
IMS = '62765742-57bf-4ccd-85e5-db8295d34ead'
LVMS = 'a3be7bf6-b5a6-4e48-833d-a1f1dd6d7a1e'
TMS = '6f78dc72-952c-47fd-889a-96c4a4049795'


sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", lgsvl.wise.SimulatorSettings.simulator_host), env.int("LGSVL__SIMULATOR_PORT", lgsvl.wise.SimulatorSettings.simulator_port))
if sim.current_scene == TMS:
    sim.reset()
else:
    sim.load(TMS)

spawns = sim.get_spawn()

state = lgsvl.AgentState()
state.transform = spawns[0]
ego = sim.add_agent(env.str("LGSVL__VEHICLE_0", VPP), lgsvl.AgentType.EGO, state)

# An EGO will not connect to a bridge unless commanded to
print("Bridge connected:", ego.bridge_connected)

# The EGO is now looking for a bridge at the specified IP and port
ego.connect_bridge(env.str("LGSVL__AUTOPILOT_0_HOST", lgsvl.wise.SimulatorSettings.bridge_host), env.int("LGSVL__AUTOPILOT_0_PORT", lgsvl.wise.SimulatorSettings.bridge_port))

print("Waiting for connection...")

while not ego.bridge_connected:
    time.sleep(1)

print("Bridge connected:", ego.bridge_connected)

print("Running the simulation...")
sim.run()

