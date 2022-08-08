#!/usr/bin/env python3
#
# Copyright (c) 2021 LG Electronics, Inc.
#
# This software contains code licensed as described in LICENSE.
#

import time
from environs import Env
import lgsvl
import requests

url = 'http://localhost/api/v1/clusters/start/apiOnly'
response = requests.get(url)

time.sleep(1)

#Vehicle Configs
VPP = '03efd1b6-0471-4e90-9372-e7e2ca1b4c25'
MultiCar1 = 'd5620330-3a85-4c60-aa41-db2e671b5110'
MultiCar2 = '9c109016-5625-4577-869e-4a2799363691'

SingleLidar1 = 'e24ef951-a337-4036-a8be-8ffb4ec6c339'
SingleLidar2 = '6066d9fa-e974-4163-b454-ae1092b4b341'

#Maps
IMS = '62765742-57bf-4ccd-85e5-db8295d34ead'
LVMS = 'a3be7bf6-b5a6-4e48-833d-a1f1dd6d7a1e'
TMS = '6f78dc72-952c-47fd-889a-96c4a4049795'

env = Env()

sim = lgsvl.Simulator(env.str("LGSVL__SIMULATOR_HOST", lgsvl.wise.SimulatorSettings.simulator_host), env.int("LGSVL__SIMULATOR_PORT", lgsvl.wise.SimulatorSettings.simulator_port))

map_seocho = TMS
robots = [
    SingleLidar1,
    SingleLidar2
]

if sim.current_scene == map_seocho:
    sim.reset()
else:
    sim.load(map_seocho)

spawns = sim.get_spawn()
spawn = spawns[0]
forward = lgsvl.utils.transform_to_forward(spawn)

for i, robot in enumerate(robots):
    state = lgsvl.AgentState()
    state.transform.position = spawn.position + (10.0 * i * forward)
    state.transform.rotation = spawn.rotation
    ego = sim.add_agent(robot, lgsvl.AgentType.EGO, state)
    print("Spawned a robot at:", state.transform.position)

    ego.connect_bridge(env.str("LGSVL__AUTOPILOT_0_HOST", lgsvl.wise.SimulatorSettings.bridge_host), env.int("LGSVL__AUTOPILOT_0_PORT", lgsvl.wise.SimulatorSettings.bridge_port))
    print("Waiting for connection...")
    while not ego.bridge_connected:
        time.sleep(1)

    print("Bridge connected:", ego.bridge_connected)

print("Running the simulation...")
sim.run()
