import re
import time
import random

def repl():
  print("\n. ݁₊ ⊹ DRESS TO DISTRESS ݁˖ . ݁\n")
  print("INSTRUCTIONS: ")
  print("MAP: ")
  map = '''                     -------------------------------------       
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
  a = input("when you're ready to play, type \"start\" (or \"quit\" to quit): ")
  while (a.strip() != "start"):
    if a.strip() == "quit":
       print(". ݁₊ ⊹ terminated ݁˖ . ݁")
       return
    a = input()
  wearing, wear_types = phase_one()
  if wearing == None and wear_types == None:
     return
  phase_two()


  
def phase_one():

    rooms = {"start":[], 
             "lobby":[], 
             "tops":[("pink off shoulder", 2, "top"), ("green floral blouse", 2, "top"), ("leather crop top", 2, "top"), ("formal white shirt", 2, "top"), ("orange tank", 2, "top"), ("oversized cream sweater", 2, "top")], 
             "bottoms":[("maroon bell bottoms", 2, "bottom"), ("black cargos", 2, "bottom"), ("skinny jeans", 2, "bottom"), ("purple leggings", 2, "bottom"), ("red plaid skirt", 2, "bottom"), ("leopard print skirt", 2, "bottom"), ("grey pencil skirt", 3, "bottom")], 
             "dresses":[("silver sequin dress", 2, "dress"), ("cream sundress", 2, "dress"), ("black bodycon", 2, "dress"), ("yellow ballgown", 2, "dress"), ("polka dot a-line", 2, "dress")], 
             "accessories":[("brown fedora", 2, "accessory"), ("denim bucket hat", 2, "accessory"), ("satin hairbow", 2, "accessory"), ("velvet wristlet", 2, "accessory"), ("pink clutch", 2, "accessory"), ("ivory belt", 2, "accessory")],
             "jewelry":[("gold hoops", 2, "jewelry"), ("leather choker", 2, "jewelry"), ("silver rings", 2, "jewelry"), ("rose gold chain", 2, "jewelry"), ("diamond studs", 2, "jewelry"), ("rainbow loom bracelet", 2, "jewelry")],
             "shoes":[("red stilettos", 2, "shoe"), ("beige sandals", 2, "shoe"), ("chunky sneakers", 2, "shoe"), ("black combat boots", 2, "shoe"), ("translucent crocs", 2, "shoe"), ("blue flip flops", 2, "shoe")]}
    wearing = []
    wear_types = []
    carrying = []
    curr_room = "start"

    enter_re = re.compile(r'^enter (start|lobby|tops|bottoms|dresses|accessories|jewelry|shoes)$') 
    view_re = re.compile(r'^view (room|inventory|outfit)$') 
    wear_re = re.compile(r'^wear ([0-9]+)$') 
    carry_re = re.compile(r'^carry ([0-9]+)$')
    edit_re = re.compile(r'(rip|tear|stretch)')
    quit_re = re.compile(r'^quit$')
    done_re = re.compile(r'^done$')

    start = time.time()
    while (time.time() - start < 360):  # pretty sure this works (just change to 360 for 6 minutes)
       r = random.randint(0,5)
       prompt = ""
       print("\n")
       if r == 0:
          prompt = "what do u wanna do? "
       elif r == 1:
          prompt = "next course of action? "
       elif r == 2: 
          prompt = "enter an action: "
       elif r == 3: 
          prompt = "periodt. what's your next move? "
       elif r == 4: 
          prompt = "slay, what r u thinking to do? "
       elif r == 5: 
          prompt = "baddie behavior, now what? "
       a = (input(prompt)).strip()
       enter_matched = enter_re.match(a)
       view_matched = view_re.match(a)
       wear_matched = wear_re.match(a)
       carry_matched = carry_re.match(a)
       edit_matched = edit_re.match(a)
       quit_matched = quit_re.match(a)
       done_matched = done_re.match(a)

       if enter_matched:
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
          else:
             print("bro that's not a room be so fr")
       elif view_matched:
          thing = view_matched.group(1)
          if thing == "room":
            items = rooms.get(curr_room)
            counter = 0
            for item in items:
                print(str(counter) + ") " + item[0])
                counter += 1
          elif thing == "inventory":
             for item in carrying:
                print(item[0])
          else:
             for item in wearing:
                print(item[0])
       elif wear_matched:        # STILL NEED TO CHECK IF ITS IN THE ROOM OR IN  CARRY
          num = int(wear_matched.group(1))

          if len(rooms.get(curr_room)) <= num:
             print("u can't wear something that doesn't exist silly")
          else:
             cloth = (rooms.get(curr_room)).pop(num)
             cloth_type = cloth[2]
             if cloth_type in wear_types:
               for i in range(0, len(wearing)):
                  if (wearing[i])[2] == cloth_type:
                     (rooms.get(curr_room)).append(wearing[i])
                     wearing[i] = cloth
             else:
                wearing.append(cloth)
                wear_types.append(cloth_type)
       elif carry_matched:
          num = int(carry_matched.group(1))
          if len(rooms.get(curr_room)) <= num:
             print("girl u can't carry nothing")
          elif len(carrying) >= 3:
             print("u can't carry that much...")
          else:
             cloth = (rooms.get(curr_room)).pop(num)
             carrying.append(cloth)
       elif edit_matched:
          return
       elif quit_matched:
          print("\n. ݁₊ ⊹ terminated ݁˖ . ݁")
          return None, None
       elif done_matched:
          print("\n. ݁₊ ⊹ PHASE ONE COMPLETE ݁˖ . ݁")
          return wearing, wear_types
       else:
          print("give an actual action pls ")

          
        
        
    print("\n. ݁₊ ⊹ PHASE ONE COMPLETE ݁˖ . ݁")
    return wearing, wear_types




def phase_two():
    pass


repl()