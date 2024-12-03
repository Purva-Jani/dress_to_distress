import re
import time
import random

# runs the game (calls both phases)
def repl():
   print("\n. ݁₊ ⊹ DRESS TO DISTRESS ݁˖ . ݁\n")
   print("INSTRUCTIONS: ")
   instructions = '''
welcome to dress to distress! here's the rundown on gameplay:

in Phase 1, u will have 6 minutes to put together an outfit, picking whichever items
u like from a variety of rooms. at any point, u can type "quit" to leave the game!

lemme give u the list of commands:
   "enter [room name]" -> lets u enter another room that is reachable from the one ur in
   "view room" -> shows u what items r in the current room
   "view outfit" -> shows u what ur currently wearing
   "view inventory" -> shows u what ur currently carrying (limit 3 items at once)
   "view map" -> shows the map again
   "view commands" -> shows the commands again
clothing related commands:
   "carry [number]" -> picks up an item from the room
   "drop [number]" -> drops an item ur carrying
   "put on [number]" -> allows u to wear something ur carrying
   "wear [number]" -> allows u to wear something from the room
   "remove [number]" -> allows u to take off something ur wearing
   "rip/tear/stretch [number]" -> edits an item ur carrying
   
if u finish before the 6 minutes, u can type "done" to end early!
otherwise, we move to Phase 2: judging

in Phase 2, u get the runway! assuming u actually have the basics of an outfit, u will
be asked to pick a pose. after that, we'll process ur outfit and give u a rating out of
5 stars. whether less stars is better or worse, well, we'll leave that up to u.

good luck!
'''
   print(instructions)
   print("MAP: ")
   map = '''   
            -------------------------------------       
            |                |                  |        
            |                \\                  |         
            |                 |                 |       
             \\     tops       |     bottoms     |       
             |                                  |       
             |              <--->               |       
             |      ^         |                 |       
   |--------------- | --------|--------\\        |       
   |        |       v         |         --------|       
   |        |                 |                 |       
   |                                            |       
   | start <-->   lobby     <-->    dresses     |       
   |                                            |       
   |        |                 |                 |       
   |        |       ^         |         --------|       
   |--------------- | --------|--------/        |       
            |       v         |                 |       
            |                 |                 |       
            |   accessories <--->   jewelry     |       
            |                 |                 |       
            |                 |                 |       
            ---\\    ^     /----------------------       
            |   --- | ----   |                          
            |       v        |                          
            |                |                          
            |     shoes      |                          
            |                |                          
            |                |                          
            ------------------                          '''
   print(map + "\n")

   # user input to start
   a = input("when you're ready to play, type \"start\" (or \"quit\" to quit): ")
   while (a.strip().lower() != "start"):
      if a.strip().lower() == "quit":
         print(". ݁₊ ⊹ terminated ݁˖ . ݁")
         return
      a = input()

   # calls Phase 1
   wearing, wear_types = phase_one()
   if wearing == None and wear_types == None:
      return
   
   # calls Phase 2
   phase_two(wearing, wear_types)
   print("\n. ݁₊ ⊹ YIPPEE, THANKS FOR PLAYING ݁˖ . ݁\n")

# Phase 1: outfit creation (dress)
def phase_one():

   # starter variables
   rooms = {"start":[], 
            "lobby":[], 
            "tops":[["pink off shoulder", 2, "top", 4], ["green floral blouse", 2, "top", 2], ["leather crop top", 2, "top", 5], ["formal white shirt", 2, "top", 5], ["orange tank", 2, "top", 1], ["oversized cream sweater", 2, "top", 4]], 
            "bottoms":[["maroon bell bottoms", 2, "bottom", 3], ["black cargos", 2, "bottom", 5], ["skinny jeans", 2, "bottom", 1], ["purple leggings", 2, "bottom", 2], ["red plaid skirt", 2, "bottom", 4], ["leopard print skirt", 2, "bottom", 3], ["grey pencil skirt", 3, "bottom", 5]], 
            "dresses":[["silver sequin dress", 2, "dress", 2], ["cream sundress", 2, "dress", 4], ["black bodycon", 2, "dress", 5], ["yellow ballgown", 2, "dress", 2], ["polka dot a-line", 2, "dress", 1]], 
            "accessories":[["brown fedora", 2, "accessory", 2], ["denim bucket hat", 2, "accessory", 3], ["satin hairbow", 2, "accessory", 4], ["velvet wristlet", 2, "accessory", 3], ["pink clutch", 2, "accessory", 2], ["ivory belt", 2, "accessory", 2]],
            "jewelry":[["gold hoops", 2, "jewelry", 5], ["leather choker", 2, "jewelry", 1], ["silver rings", 2, "jewelry", 5], ["rose gold chain", 2, "jewelry", 4], ["diamond studs", 2, "jewelry", 4], ["rainbow loom bracelet", 2, "jewelry", 1]],
            "shoes":[["red stilettos", 2, "shoe", 3], ["beige sandals", 2, "shoe", 2], ["chunky sneakers", 2, "shoe", 4], ["black combat boots", 2, "shoe", 3], ["translucent crocs", 2, "shoe", 1], ["blue flip flops", 2, "shoe", 1]]}
   
   wearing = []
   wear_types = []
   carrying = []
   curr_room = "start"

   # command regex
   enter_re = re.compile(r'^enter\s+(start|lobby|tops|bottoms|dresses|accessories|jewelry|shoes)$') 
   view_re = re.compile(r'^view\s+(room|inventory|outfit|map|commands)$') 
   puton_re = re.compile(r'^put on\s+([0-2])$') 
   wear_re = re.compile(r'^wear\s+([0-9]+)$')
   remove_re = re.compile(r'^remove\s+([0-9]+)$')
   carry_re = re.compile(r'^carry\s+([0-9]+)$')
   drop_re = re.compile(r'^drop\s+([0-9]+)$')
   edit_re = re.compile(r'^(rip|tear|stretch)\s+([0-9]+)$')
   quit_re = re.compile(r'^quit$')
   done_re = re.compile(r'^done$')

   # run for 6 minutes
   start = time.time()
   while (time.time() - start < 360):

      # randomize the prompt
      r = random.randint(0,10)
      prompt = ""
      print("\n")
      if r == 0:
         prompt = "what do u wanna do? "
      elif r == 1:
         prompt = "next course of action? "
      elif r == 2: 
         prompt = "enter an action: "
      elif r == 3: 
         prompt = "periodt. what's your move? "
      elif r == 4: 
         prompt = "slayed, what r u thinking to do? "
      elif r == 5: 
         prompt = "baddie, now what? "
      elif r == 6: 
         prompt = "ate, now pick an action: "
      elif r == 7: 
         prompt = "gimme a command: "
      elif r == 8: 
         prompt = "girlboss, what u gonna do? "
      elif r == 9: 
         prompt = "queen, tell me an action: "
      elif r == 10: 
         prompt = "ok serve, what's the plan? "
      a = (input(prompt)).strip().lower()

      # command matches
      enter_matched = enter_re.match(a)
      view_matched = view_re.match(a)
      puton_matched = puton_re.match(a)
      wear_matched = wear_re.match(a)
      remove_matched = remove_re.match(a)
      carry_matched = carry_re.match(a)
      drop_matched = drop_re.match(a)
      edit_matched = edit_re.match(a)
      quit_matched = quit_re.match(a)        
      done_matched = done_re.match(a)

      items_in_room = rooms.get(curr_room)

      if enter_matched: # moving rooms

         to_room = enter_matched.group(1)
         if curr_room == "start":
            if to_room == "start" or to_room == "lobby":
               curr_room = to_room
            else:
               print("you can't reach " + to_room + " from start")
         elif curr_room == "lobby":
            if to_room == "lobby" or to_room == "tops" or to_room == "dresses" or to_room == "accessories":
               curr_room = to_room
            else:
               print("you can't reach " + to_room + " from the lobby")
         elif curr_room == "tops":
            if to_room == "tops" or to_room == "bottoms" or to_room == "lobby":
               curr_room = to_room
            else:
               print("you can't reach " + to_room + " from tops")
         elif curr_room == "bottoms":
            if to_room == "bottoms" or to_room == "tops":
               curr_room = to_room
            else:
               print("you can't reach " + to_room + " from bottoms")
         elif curr_room == "dresses":
            if to_room == "dresses" or to_room == "lobby":
               curr_room = to_room
            else:
               print("you can't reach " + to_room + " from dresses")
         elif curr_room == "accessories":
            if to_room == "accessories" or to_room == "lobby" or to_room == "jewelry" or to_room == "shoes":
               curr_room = to_room
            else:
               print("you can't reach " + to_room + " from accessories")
         elif curr_room == "jewelry":
            if to_room == "jewelry" or to_room == "accessories":
               curr_room = to_room
            else:
               print("you can't reach " + to_room + " from jewelry")
         elif curr_room == "shoes":
            if to_room == "shoes" or to_room == "accessories":
               curr_room = to_room
            else:
               print("you can't reach " + to_room + " from shoes")
      
      elif view_matched: # viewing something

         thing = view_matched.group(1)
         if thing == "room":
            counter = 1
            for item in items_in_room:
               print(str(counter) + ") " + item[0])
               counter += 1
         elif thing == "inventory":
            counter = 1
            for item in carrying:
               print(str(counter) + ") " + item[0])
               counter += 1
         elif thing == "outfit":
            counter = 1
            for item in wearing:
               print(str(counter) + ") " + item[0])
               counter += 1
         elif thing == "map":
            map = '''   
            -------------------------------------       
            |                |                  |        
            |                \\                  |         
            |                 |                 |       
             \\     tops       |     bottoms     |       
             |                                  |       
             |              <--->               |       
             |      ^         |                 |       
   |--------------- | --------|--------\\        |       
   |        |       v         |         --------|       
   |        |                 |                 |       
   |                                            |       
   | start <-->   lobby     <-->    dresses     |       
   |                                            |       
   |        |                 |                 |       
   |        |       ^         |         --------|       
   |--------------- | --------|--------/        |       
            |       v         |                 |       
            |                 |                 |       
            |   accessories <--->   jewelry     |       
            |                 |                 |       
            |                 |                 |       
            ---\\    ^     /----------------------       
            |   --- | ----   |                          
            |       v        |                          
            |                |                          
            |     shoes      |                          
            |                |                          
            |                |                          
            ------------------                          '''
            print(map)
         else:
            instructions = '''
"enter [room name]" -> lets u enter another room that is reachable from the one ur in
"view room" -> shows u what items r in the current room
"view outfit" -> shows u what ur currently wearing
"view inventory" -> shows u what ur currently carrying (limit 3 items at once)
"view map" -> shows the map again
"view commands" -> shows the commands again
"carry [number]" -> picks up an item from the room
"drop [number]" -> drops an item ur carrying
"put on [number]" -> allows u to wear something ur carrying
"wear [number]" -> allows u to wear something from the room
"remove [number]" -> allows u to take off something ur wearing
"rip/tear/stretch [number]" -> edits an item ur carrying 
"done" -> end Phase 1 before the 6 minutes are over
"quit" -> exit the game'''
            print(instructions)
      
      elif puton_matched: # wearing something from the inventory

         num = int(puton_matched.group(1)) - 1
         if len(carrying) <= num or num < 0:
            print("u gotta carry something before u can put it on")
         else:
            cloth = carrying.pop(num)
            cloth_type = cloth[2]
            if cloth_type in wear_types:
               for i in range(0, len(wearing)):
                  if (wearing[i])[2] == cloth_type:
                     items_in_room.append(wearing[i])
                     wearing[i] = cloth
            else:
               wearing.append(cloth)
               wear_types.append(cloth_type)
      
      elif wear_matched: # wearing something from the room

         num = int(wear_matched.group(1)) - 1
         if len(items_in_room) <= num or num < 0:
            print("u can't wear something that's not in the room")
         else:
            cloth = items_in_room.pop(num)
            cloth_type = cloth[2]
            if cloth_type in wear_types:
               for i in range(0, len(wearing)):
                  if (wearing[i])[2] == cloth_type:
                     items_in_room.append(wearing[i])
                     wearing[i] = cloth
            else:
               wearing.append(cloth)
               wear_types.append(cloth_type)
      
      elif remove_matched: # removing something from the outfit

         num = int(remove_matched.group(1)) - 1
         if len(wearing) <= num or num < 0:
            print("u can't remove something ur not wearing")
         else:
            cloth = wearing.pop(num)
            cloth_type = cloth[2]
            wear_types.remove(cloth_type)
            items_in_room.append(cloth)
      
      elif carry_matched: # carrying something from the room

         num = int(carry_matched.group(1)) - 1
         if len(items_in_room) <= num or num < 0:
            print("girl u can't carry something that doesn't exist")
         elif len(carrying) >= 3:
            print("u can't carry that much...")
         else:
            cloth = items_in_room.pop(num)
            carrying.append(cloth)
      
      elif drop_matched: # dropping something from the inventory 

         num = int(drop_matched.group(1)) - 1
         if len(carrying) <= num or num < 0:
            print("u can't drop something ur not carrying")
         else:
            cloth = carrying.pop(num)
            items_in_room.append(cloth)
      
      elif edit_matched: # ripping/tearing/stretching something from the inventory

         num = int(edit_matched.group(2)) - 1
         if len(carrying) <= num or num < 0:
            print("u can't " + edit_matched.group(1) + " something ur not carrying")
         else:
            perc = ((carrying[num])[1])
            if (perc > 0):
               perc -= 1
               if (perc == 1):
                  (carrying[num])[3] += 1
               else:
                  (carrying[num])[3] -= 2

      elif quit_matched: # exiting the game

         print("\n. ݁₊ ⊹ terminated ݁˖ . ݁")
         return None, None
      
      elif done_matched: # finishing early

         print("\n. ݁₊ ⊹ PHASE ONE COMPLETE ݁˖ . ݁\n")
         return wearing, wear_types
      else:
         print("give an actual action pls ")

   print("time up!")
   print("\n. ݁₊ ⊹ PHASE ONE COMPLETE ݁˖ . ݁\n")
   return wearing, wear_types

# Phase 2: judging (distress)
def phase_two(wearing, wear_types):

   # incomplete outfit
   if (("top" not in wear_types or "bottom" not in wear_types) and ("dress" not in wear_types)):
      print("pls, we wanted a bad outfit not no outfit...")

   else:

      # user selects runway pose
      print("time to channel ur inner model")
      a = (input("select a runway pose (enter an integer from 1 to 6): ")).strip()
      while (a != "1" and a != "2" and a != "3" and a != "4" and a != "5" and a != "6"):
         if a == "quit":
            print(". ݁₊ ⊹ terminated ݁˖ . ݁")
            return
         a = (input("por favor, an integer from 0 to 5: ")).strip()

      if a == "1":
         pose = '''          
      +-------+
      |       |
      |       |
      |       |
      +-------+
          |
        /-|-\\
     /--  |  --\\
   --     |     --
   ---\\   |   /---
       ---|---
          |
         / \\
        /   \\
       /     \\
      /       \\
     /         \\
    -           -'''
         
         print(pose)
         print("oh u hit that 28... but let's see how u did: ")

      elif a == "2":
         pose = '''
       +-------+
       |       |
     - |       |
   -/  |       |
   --  +-------+
     \\---  |
         \\-|-\\
           |  --\\
           |     --
           |   /---
           |---
           |
          | |
          / \\
         |   |
         /   \\
        |     |
        |     |'''
         
         print(pose)
         print("ok i see u baddie... now onto judging: ")

      elif a == "3":
         pose = '''
        |     |
        |     |
         \\   /
         |   |
          \\ /
          | |
           |
           |
           |
           |
           |
       /---|---\\
   ----    |    ----
   |   +-------+   |
   |   |       |   |
   |   |       |   |
   |   |       |   |
   |   +-------+   |'''
         
         print(pose)
         print("woah headstand slay... but its the outfit that matters: ")

      elif a == "4":
         pose = '''
             +-------+
             |       |
             |       |
             |       |
             +-------+
                 |
               /-|-\\
            /--  |  --\\
          --     |     --
                 |
                 |
   -------------   --------------'''

         print(pose)
         print("the splits?!?!?!... let's see the fit tho: ")

      elif a == "5":
         pose = '''
     +-------+
     |       |
     |       |
     |       |
     +-------+
         |
        /|-\\
       | |  --\\
       / |     --
      /  |   /---
     |   |---
   --    |
        | |
        / \\
       |   |
       /   \\
      |     |
      |     |'''

         print(pose)
         print("ok highkey ate... but did the outfit eat: ")

      elif a == "6":
         pose = '''
     +-------+
     |       |
     |       |
     |       |
     +-------+
         |
        /|\\
       | | |
       / | \\
      /  |  \\
     |   |   |
   --    |    --
        | \\
        |  \\
        |   \\
        |    \\
        |     \\
        |      -'''

         print(pose)
         print("my queen... who is about to be judged: ")

      time.sleep(2)
      print("\nprocessing fit...")
      time.sleep(2)
      print("\nanalyzing slay...")
      time.sleep(2)
      print("\nthis is distressing...")
      time.sleep(2)
      
      # autograding
      print("")
      count = 0
      for item in wearing:
         count += item[3]
      count /= len(wear_types)
      count = round(count)
      if count <= 0:
         count = 1
      elif count >= 6:
         count = 5
      
      print("your rating: ")
      for i in range(count):
         print("★", end = "")
      for i in range(5 - count):
         print("☆", end = "")

      return

repl()