
# TODO:
# - Create max amount of loot that player can carry (do testing towards end of development)
# - Create the "story" around the use of the MOU (alien general remaining)
# - Create death locations on electrical fence by giant frog-like creatures
# - Place each class in escape.py into separate *.py files
# - Add some explanation to how the player finds the direction back to earth

import os

class Map:
	def __init__(self):
		self.c_row = 10			# Initial row of player.
		self.c_col = 10 			# Initial column of player.
		self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
			       [1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1],
			       [1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1],
			       [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
			       [1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
			       [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1],
			       [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1],
			       [1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1],
			       [1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
			       [1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1],
			       [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
			       [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
		
		self.num_locations = len(self.map) * len(self.map[0])		# Number of total locations in the world.
		self.player_indicator = 8									# Indicating where the player is (dev).

		self.climb_tree_location = (10, 6)							# Location from which the tree can be climbed.
		self.tree_location = (10, 7)								# Location of the actual tree hiding the arrows.
		self.supplies_location = (8, 1)								# Location of abandoned supplies hiding the antidote.
		self.door_location = (5, 4)									# Location of the door hiding the rope.
		self.hook_grenade_location = (3, 10)						# Location of alien type hook and grenade.
		self.MOU_location = (1, 10)									# Location of the Military Operating Unit.
		self.venom_location = (10, 9)								# Location of venomous plant.
		self.climb_cliff_location = (10, 10)						# Location of bottom of cliff near the end of the game.
		self.cliff_location = (9, 10)								# Location of top of cliff the end of the game.
		self.death_locations = [(10, 1), (10, 2), (10, 3), (11, 4), (11, 5), (11, 6), (5, 10), (6, 8), (6, 10), (7, 10)]

		self.has_moved = True 						# Boolean variable that gets set True whenever the player moves.
		self.has_removed_supplies = False 			# Boolean variable that gets set True when player removes supplies.
		self.has_destroyed_door = False 			# Boolean variable that gets set True when player destroys the door.
		self.has_been_stung = False 				# Boolean variable that gets set True when player gets stung.
		self.has_injected_antidote = False 			# Boolean variable that gets set True when player injects antidote.
		self.has_disabled_AA = False

		self.iters_num_after_sting = 0 				# Counts while-iterations after player gets stung.

	# Function that displays the map.
	def view_map(self):
		print "\n"

		for i in range(len(self.map)):
			print self.map[i]
			


class Items(Map):
	def __init__(self):
		Map.__init__(self)
		self.inventory  = []			# List to hold players inventory.
		self.inventory_capacity = 3		# Carrying capacity of player.
		self.attainable_items = {}		# Dictionary to hold items in the world.

	# Function that adds item to inventory and removes it from the world.
	def add_item(self, item, location):
		self.inventory.append(item)
		deletion_index = self.attainable_items[location].index(item)
		del self.attainable_items[location][deletion_index]

	# Function that removes item from inventory and adds to world.
	def remove_item(self, item, location):
		self.inventory.remove(item)
		self.attainable_items[location].append(item)

	# Function that displays the players inventory.
	def view_inventory(self):
		if (len(self.inventory) != 0):
			print "\nYour inventory:"
			for i in range(len(self.inventory)):
				print str(i + 1) + ") " + self.inventory[i].title()
				
		else:
			print "Your inventory is empty"

	# Function initiating attainable_items dictionary.		
	def assign_empty_items_arrays(self):
		for i in range(0, len(self.map)):
			for j in range(0, len(self.map[i])):
				self.attainable_items[(i, j)] = []

	# Function for initiating interactable items.			
	def add_items_to_world(self):
		self.attainable_items[self.door_location].append("rope")
		self.attainable_items[self.hook_grenade_location].append("hook")
		self.attainable_items[self.hook_grenade_location].append("grenade")
		self.attainable_items[self.tree_location].append("sniper")
		self.attainable_items[self.supplies_location].append("antidote")


class Messages(Map):
	def __init__(self):
		Map.__init__(self)
		self.welcome ="""\n
-------------------------------------------------------------------------
---------This is the text based adventure game 'Escape'.-----------------
---------An experiment with your teleporter went horribly----------------
---------wrong. It brought you to a prevoiusly unknown part--------------
---------of the galaxy. You are on completely foreign territory.---------
---------You must stay cool and move smart to stay alive.----------------
---------After the failed teleporter, experiment you are stranded--------
---------in a large forest on the planet 'Zeon' populated by aliens!-----
---------Perfect your playthrough by completing the game with the--------
---------fewest amount of commands to earn the most adventurer points----
---------Start exploring to find various items to help you get-----------
---------off this alien planet alive.------------------------------------
-------------------------------------------------------------------------
---------Use the command help any time during the game to----------------
---------get information about how to play.------------------------------
-------------------------------------------------------------------------\n"""
		self.arrival_info = {(1, 1)  : "You have arrived at the campsite. It seems abandoned;\nthere is nobody around, but the fire is still burning, implying\nthey didn't leave a long time ago. The camp is set up in a\ncorner meaning the only way to go is back in\ndirection east. You notice that an alien type computer\nis left behind. Seems like it belonged to someone involved in\ncontrolling the Military Operating Unit (A large\nsupercomputer used by the aliens to operate all military related\nactivity). This alien programmer was working on updating the\ndefense systems for their planet. He must have left in a hurry as\nthe source code is still visible on screen. Some of the code reads:\n\nLINE 714: AA_defense.enabled = TRUE\nLINE 715:\nLINE 716: if ((AA_defense.enabled) and (enemy in AA_defense.sight)):\nLINE 717:    AA_defense.enable_aim(ALL_TURRETS)\nLINE 718:    AA_defense.fire_at_target(enemy)\n\nIf you find the military operating unit and gain access to it, you\ncould probably change the top line of this code to deactivate the\nalien anti air defense mechanisms.",
			(1, 2)  : "To the east you see where all the light came from; A little\nalien campsite. A path also leads to the south and to the east. To the\nnorth a very wide and fast flowing river consisting of acid blocks your way.",
			(1, 3)  : "You are still walking along the acid river to the north. You are\nnow directly north of the meteor crater. This meteor left a\nserious scar in the terrain! The crater is nearly 50 meters deep.",
			(1, 4)  : "This is the eastern end of the acid river directly to the north.\nCliffs block you way to the east. The path is leading both south and west.",
			(1, 9)  : "The energy shield and the large construction forces you to go\neither back south towards the gate or east towards the inner\nnorth-eastern corner of the complex. To the east you spot high-tech\nscreens of some sort. Best to check it out.",
			(1, 10) : "You found the terminal! This is where the supercomputer is\ntold what to do. Now you have the oppurtunity to reprogram it to\nyour advantage. Program the supercomputer so that it wont shoot you\ndown if you ever manage to find a way off this planet. If you dont\nalready have the line of code to be changed, aquire it from the\nlast alien programmerwho was working here. He supposedly went up north\n-west somewhere. However knowing what line in what file to change is\nnot enough; using the terminal itself is not straight-forward and\nrequires specific instructions/commands, so if you don't have the\ncorrect commands, using the terminal is near impossible (but you could\ntry). Instructions on how to use the terminal/console are, for security\nreasons, only available to the generals of the military. The alien\ngenerals tend to use a place far south-east as their base of operations.\nWhen aquired both the knowlegde of what line in what file to\nchange and how to use the terminal to do this, then use the terminal\nto disable the anti-air turrets/missiles.",
			(2, 2)  : "This is a rather narrow path leading towards something that\nmight not want to be found. Stay alert! Directly to your east you\nsee the large crater made by a striking meteor. The path goes north-south here.",
			(2, 4)  : "There are unclimbable cliffs to the east. To the west there is a\nlarge crater made by an erlier striking meteor. The\ncrater still feels hot. The path goes north-south here.",
			(2, 7)  : "You stand before a giant gate which separates the forest path from\nwhats behind the high-tech energy shield! An unclimbable cliff blocks\nyour way to the west and north. South leads back to the\nthree-way jucntion. To the east you see a small slip\nin the giant gate, which is clearly made\nfor something a lot bigger than you.",
			(2, 8)  : "You are now directly on the inside of the energy shield. You could\ngo back west through the slip in the gate. To the east the\nthere is a small junction right up ahead.",
			(2, 9)  : "Here the path leads either back west towards the gate, or either to\nthe north or south. Both these paths eventually turn east. Directly\neast you see what could bee the reason behind the energy shield;\nA massive supercomputer in the middle of the forest! It's of the\nsize of a football field and by the looks of it, it seems to be\nsome sort of military operating unit for what ever higly advanced\nspecies that populates this planet.",
			(3, 1)  : "This is the very north end of north-south road, a road which extends\nfor several miles along the foot of the infamous Mount Doom\nto the west. An unclimbable mountain. The path also\ncontinues to the east. To the north, although\nuntraversable, you see some ligths trhough the trees.",
			(3, 2)  : "You are at a three-way junction paths is leading north,\nwest and east. To the north-west you glimpse some lights\nthrough the dense forest. Could be interesting.",
			(3, 3)  : "You are walking on a path streching east-west. To the south, the forest is too dense to move through. To the north a crater from a earlier meteor strike.",
			(3, 4)  : "You have arrived at a four way junction. There are paths leading\nin all directions. A glimpse of the cabin is barely visible to\nthe south. To the north the path eventually turns eastward.",
			(3, 5)  : "You have arrived at a very open clearing in an otherwise\nrather tight forest. The path continues in direction east-west\nwith unclimbable cliffs north and untraversable forest to the south.",
			(3, 6)  : "You are on a quite wide path. There is dense forest to the\nsouth and unclimbable cliffs to the north. The path is very\nlong and leads east-west. To the west,you see a large\nopen field which the path cuts straight through.",
			(3, 7)  : "You have arrived at a three-way junction. Directly to your\neast a tall and mysteroius energy shield blocks your way. A path\nleads to the south as well as to the west and north. Northwards you\nspot something that seems to be an entrance through the energy shield.",
			(3, 9)  : "Here the massive construction leads you in two directions;\neither back north closer to the gate or east further into the large\nconstruction. To the south and west the tall and unbreakable energy\nshield blocks your way.",
			(3, 10) : "You have arrived at the inner south-eastern corner of the\nconstruction inside the energy shield. It seems like a dead\nend, but it seems as if the last alien maintaining this section\nof thesupercomputer left some of his equipment; a hook and a\ngrenade. Both these items might help in suriving this difficult\nsituation you find yourself in.",
			(4, 1)  : "On north-south road. The road is quite wide and seems to\nhave been made for some sort of transportation for the locals.\nDense forest to the east and the terryfying sight of Mount Doom to the west.",
			(4, 4)  : "You're on a narrow pathway. There are trees hanging over you\nfrom both sides. The forest is too dense to go either east\nnor west. The path goes north-south here.",
			(4, 7)  : "You are on a path that goes purely north-south. The forest to the west is\nway too dense to traverse. Also one would risk ending up i a\nconfrontation with the unknown wildlife. To the east there\nis you see the fascinating energyshield that obvoiusly\nhides something. The entrance can't be far away.",
			(5, 1)  : "You are walking on north-south road. Not much happening here.\nQuite a boring road really. Your blocked in both direction west\nand east by Mount Doom and dense forest respectively.",
			(5, 3)  : "This is the north-west corner of the cabin. Here the forest blocks you\nfrom going both north and west. East will lead you to the\nmain entrance of the cabin. South will lead you to the west side of the cabin.",
			(5, 4)  : "You're standing north of a quite small alien construction,\nsimilar to a cabin. The cabin is heavily damaged by a rock\navalanche from the majestic Mount Doom located further west. The only\nentrance to the cabin; a thorughly sealed off metal door, looks\nhard to break, but not impossible with enough energy. A pathway leads to\nthe north. To the east and west there are ways to get around the cabin.",
			(5, 5)  : "You're at the north-east corner of the house. The forest is unwalkable\nto the north and east. Going south gets you to the east side of the cabin.\nGoing west gets you to the main entance of the cabin.",
			(5, 7)  : "There is very dense forest with sounds of a rich wildlife to your west.\nYou are on a path stretching north-south, although there\nis a path leading to the east as well.",
			(5, 8)  : "You are on the north side of a pack of giant snake-like creatures\nwho are closed up by a large electrical fence. To the north there\nis very interestening and scary-looking energy shield.\nIt may be there to potect someting. There should be a way\ninside around here somewhere. The path leads east-west.",
			(5, 9)  : "The path turns here. Meaning it leads west-south. To the north you\nsee the very cool energyshield blocking both visual and physical access.\nThe entrance must be in the vicinity. To the east there is a majestic\nwaterfall which ends down in a cave, that blocks your way.",
			(6, 1)  : "This is the infamous north-south road right under Mount Doom.\nThis roads extends along the foot of the mountain. Mount Doom\nis way too steep and slippery to climp.\nTo the west, a path leads back to the cabin.",
			(6, 2)  : "You are on a narrow pathway that separates the avalanche decay\nfrom the dense forest. Right west of you is the\ninfamous north-south road rigth at the foot of the unclimbable,\ntall and majestic Mount Doom. To the east you see the wooden cabin and how\nit just survived the avalanche froom Mount Doom.",
			(6, 3)  : "You have arrived at the west side of the wooden cabin.\nOn this side there is a window high up, displaying a\nlittle girl's teddy bears. To the north and south\nthere are ways to get around he cabin. To the west a pathway\nleads towards a long road which goes north-south.",
			(6, 5)  : "This is the eastern side of the cabin. Here there are ways to get\naround the cabin to the north and south.\nThe cabin has no entrance at his side. To the east there's\nan opening between the rocks and the dense forest.",
			(6, 6)  : "You are squeezed inbetween the rocks to your east and the\ntrees to the north. Direction west leads back to the cabin,\nwhile moving east will get you to a path leading up north.",
			(6, 7)  : "The path leads north here. You could also go west between\nthe trees and the pile of rocks, to get back to the cabin.\nRock debree to the south blocks your way there. To the east you\nsee a fenced up pack of extremely wierd looking giant-snake\nlike creatures. The electrical fence prevents you from moving this way.",
			(6, 9)  : "You are still along the huge and beautiful waterfall extending\nnorth-south. You are now on the east side of the electrically\nfenced up snake-like creatures. They seem to be\nresting and show no aggression at all.",
			(7, 1)  : "You're still on the north-south road extending along the\nfoot of the unclimbable Mount Doom. Directly to your\neast is the avalanche that nearly destroyed the cabin.",
			(7, 3)  : "This is the south-west corner of the cabin. To the east is the\nsouthern wall of the cabin. To the north is the western\nside of the cabin. A big pile of rocks from an avalanche\nthat almost destroyed the cabin, blocks your way both south and west.",
			(7, 4)  : "The south side of the cabin. The sun has caused the paint to\nfaid away on this side. A slip in the rock pile to\nthe south, is just wide enough to move through. To the west and east\nthere are ways to get around the cabin.",
			(7, 5)  : "This is the south-east corner of the cabin. At this corner,\nthe avalanche that caused the rock pile, has heavily damaged the cabin.\nHere the big pile of rocks are blocking your way to the south and east.\nWest leads you to the southern side, going north leads you to the eastern side.",
			(7, 8)  : "You are now at the south side of the electrical fence which\nbehind you see giant snake-like creatures. To the west, the\nhuge pile of rocks separates you from a direct route back to\nthe cabin. There is a path that leads south and east.",
			(7, 9)  : "You are at the very south end of the beautiful waterfal to the east.\nSwimming is not an option as the waterfal is ironicly\nconstructed of strong acid. To the south there are dense\nforest blocking your way. A path leads both north and west.",
			(8, 1)  : "On North-south road. Mount Doom to the west. Large\nrocks that separate you and the cabin is piled up to the east.\nThey are too heavy to move, or to navigate through. However at\nthe side of the road, which seem to be built for transportation\nby the indigenous alien race, you spot a pile of damaged supplies\nfrom some sort of veichle. Among the supplies you glimpse some\nsort of liquid medicine; an antidote.",
			(8, 4)  : "You are now squeezed inbetween the rock debree from the\navalnche from Mount Doom. It's not a comfortable walk\nat all, and you should quickly get through before\nrisking having any rocks fall down on you.",
			(8, 8)  : "This is a path extending north-south. The huge pile of rocks still\nblocks you from moving west. To the east there is imprevious forest\nas far as they eye can see.",
			(9, 1)  : "This is the very south of the north-south road. To he north the\nnorth-south road extends all the way along the foot of the\nmajestic and unclimbable Mount Doom. The avalanche from\nMount Doom made the huge and very steep ravine to the south.\nTo the east a path embedded in the huge pile of rocks\nextends along the very edge of the ravine.",
			(9, 2)  : "Don't loose balance at this point! The edge is very\nnarrow here and the ravine doesen't look like it\ngives a warm welcome to anyone unlucky enough to fall down.",
			(9, 3)  : "You're bravely on the edge of the ravine with your back\npushed up against the pile of rocks. To the east the edge looks\nless dangerous and merges in to a regular path. Although to the west,\nthe path gets even narrower. Only the ones with\nlittle to nothin to loose will even think about going over there.",
			(9, 4)  : "You stand at a three-way junction where a slip in\nthe rock pile to the north, leads back to the house. To the west there's a\nledge along a huge ravine and to the east a giant anthill\nblocks your way. Go south to move around the anthill.",
			(9, 6)  : "You are now at the east side of the giant anthill\nblocking your visibility to the west. A path leads south briefly\nbefore being swallowed by the Drowner Swamp. There are also a\npath to the east, but to the north, you're blocked by the massive\npile of rocks from the avalanche from Mount Doom.",
			(9, 7)  : "You stand directly north of a large and old tree.\nIt looks hard to climb from here, but there seems to be an esier\nway on the west side of the tree. Right east\nyou spot a junction with several options. To the north\nthe rocks are too dominant to move through.",
			(9, 8)  : "This is a three-way junction with paths leading north and east.\nTo the south there seems to be a rather mysterious path. It's a\nlot narrower than ususal paths and doesn't seem to friendly, but\nif thread carefully it might be worth a look.",
			(9, 10) : "You made it to the top of the cliff without falling. What\nyou thought would be an ancient human-made temple turns out to\nbe a fully functioning alien spaceship right next to you! And\nthe creature you glimpsedfrom the bottom of the cliff, is a huge,\nangry looking alien, who saw you arrive at their planet and\nbelieves you are hostile. He does not look friendly, is impossible\nto communicate with and willing to to anything to protect his\npeople from harm. Suddenly the alien reaches for a weapon and\nprepares to shoot you. Climb back down or quickly eliminate\nhim before you're dead.",
			(10, 4) : "You barely see the cabin through some rocks to the north.\nThe huge ravine caused by an avalanche from Mount Doom\nis visible to the west. To the south the huge Drowner Swamp\nextends over a large area. The path leads north and east here.",
			(10, 5) : "You're directly south of the anthill. The path leads\neast-west. The very hostile Drowner-Swamp is dangerously\nclose to the south. Do not fall in or you will\nsuffer the painfull death of drowning.",
			(10, 6) : "You're options are either to move north or west. Direction south is definetly\nnot recomended due to the very close and vast Drowner Swamp\nthat drag down nearly anything. A large, unusual and very old\ntree prevents you from going directly east.\nThe tree looks climbable from this side.",
			(10, 7) : "You reached the top of the tree to find an alien snipers nest.\nHere you see an abandoned sniper earlier used by the alien.\nThis could come to great use if you were unlucky enough to come\na cross a hostile alien later. Grab the sniper to be able to defend yourself.",
			(10, 8) : "What a hostile path! Something doesn't want you here. To the\nwest you see a large and very old tree. It's unclimbable from\nhere, but it looks more promising on the west side. To the north\nyou go back to the three-way junction, although to the east the\nnarrow path continues into darkness.",
			(10, 9) : "An extremely venomous snake-like creature launches out of the bush and\nbites you! The large snake supposedly where to be locked up inside an\nelectrical fence somwhere further north. It must have escaped its\ncaptivity. The venom is very dangerous and will lead to death within\na short amount of time.",
			(10, 10): "You're now in place where the path only leads back west.\nThere is dense forest to the south and east. Right before you,\nto the north, you se a terrifingly steep cliff with. You hear\nscary sounds coming from 50 meters above you. Looking straight\nup, you also barely see a glimpse of a large and mysterious creature.\nThe cliff looks climbable if equipped with a rope and climbing shoes."}
		
		self.new_item_at_location = "\nOn the ground you also see the earlier dropped "
		self.tree_message_updated = "You've reached the snipers nest in the top of the tree again."
		self.supplies_message_01 = "The supplies are successfully removed and before your eyes is a rare\nand very important antidote if one wishes to survive on Zeon.\nIt's an antidote for the venom of a common and dangerous giant snake.\nIf you were to get bitten by the snake-like creature, immediately inject\nthe andtidote to survive."
		self.supplies_message_02 = "On north-south road. This is were you earlier found the antidote."
		self.door_message_01 = "The door is now broken! Unfortunately the entire inside of the cabin is\ndestroyed and buried by the avalanche from Mount Nev, but in the doorway\nright next to you, there's strong-looking rope that may be useful."
		self.door_message_02 = "This is the north side of the cabin where you earlier found the rope in\nthe doorway. A pathway leads to the north. To the east and west there\nare ways to get around the cabin."
		self.hook_message_01 = "South-east corner of supercomputer complex. this is where you found\neither the hook, grenade or both earlier."
		self.venom_message_01 = "The mysterious path is here very narrow with extremely dense forest\nboth to the north and south. You see small bits of ruins of an ancient\ntemple along the path. This path seems to be leading to something big. You\ncan go back west or go east into darkness, to what seems to be something\nthat leads towards a temple."

		self.MOU_prompts = ["HELLO--: ", "MOU--: ", "MOU--: ", "MOU--: ", "NevCee-SCRIPT--: ", "NevCee-SCRIPT--: ", "NevCee-SCRIPT--: ", "NevCee-SCRIPT--: ", "LINE 714: ", "MOU--: "]
		self.MOU_feedback_01 = "\n--------------------------------------------\nWELCOME TO THE MILITARY OPERATING UNIT.\nPLEASE TELL THE CONSOLE WHAT YOU WANT TO DO.\n--------------------------------------------\n"
		self.MOU_feedback_02 = "\n----------------------\nNevCee SCRIPT ENABLED.\n----------------------\n"
		self.MOU_feedback_03 = "\n------------------------------------------------------------------------\nACCORDING TO PRE-FILE SCRIPT:\n- LINE 714 IS DELETED\n- CURRENT ACTIVE LINE IN CONSOLE IS NOW 714\n- THE MOU WILL EXIT AA_file.nc AFTER LINE 714 IS WRITTEN USING THE OneLineWrite FUNCTION.\nENTERING AA_file.nc\n------------------------------------------------------------------------\n"
		self.MOU_feedback_04 = "\n-------------------------\nWROTE TO LINE 714\nEXITING AA_file.nc\nRETURNING TO MOU-CONSOLE:\n-------------------------\n"
		self.MOU_feedback_05 = "\n------------------\nAA-defense systems diabled.\nEXITING MOU.\n------------------\n"

		self.successfull_injection = "The needle gives you great pain, but the antidote seem to have\nbattled off the poison and you have successfully survived the\nvenomous plant encounter!"

		self.death_01 = "You walked off the cliff and fell down the ravine to your death!"
		self.death_02 = "The Drowner swamp is unforgiving and is inescapable causing you to drown!"
		self.death_03 = "You tried to traverse through the waterfall to find\nyourself slowly etching to death due to the strong acid!"
		self.death_04 = "You walked right into the electrical fence that houses the giant snakes.\nThe strong electric current is too much for you and you fall down and die."
		self.death_antidote = "You injected the antidote without having been exposed\nto any venom. This poses a lethal effect on your body and you\ndie of the overdose!"
		self.death_venom = "\nThe venom spreads through your body causing you massive pain and then death."
		self.death_info = {(10, 1): self.death_01, (10, 2): self.death_01, (10, 3): self.death_01, (11, 4): self.death_02, (11,5): self.death_02,
						   (11, 6): self.death_02, (5, 10): self.death_03, (6, 8): self.death_04, (6, 10): self.death_03, (7, 10): self.death_03}

	# Function for removing part of arrival info indicating earlier dropped items.					   
	def remove_relevant_sentence(self, item, location):
		sub_text = self.new_item_at_location + item + "."								# The relevant part of arrival info at location.
		start_of_sub = self.arrival_info[location].index(sub_text)						# Index in arrival info at which the sub starts.
		end_of_sub = start_of_sub + len(sub_text)										# Index in arrival info at which sub ends (+1).
		first_part_of_edited = self.arrival_info[location][:start_of_sub]				# The part of arrival info before sub starts.
		last_part_of_edited = self.arrival_info[location][end_of_sub:]					# The part of arrival info after sub ends.
		edited_text = first_part_of_edited + last_part_of_edited						# Part before sub joint with the part after.
		self.arrival_info[location] = edited_text										# Updating arrival_info at the relevant location.

	def display_arrival_message(self, location):
		print self.arrival_info[location]												# Display arrival_info at relevant loction.
		
	def display_death_message(self, location):
		print self.death_info[location]													# Display death_info at relevant location.
		
	def update_arrival_item_info(self, location, item):
		self.arrival_info[location] += self.new_item_at_location + item + "."			# Update arrival info when player drops an item at location.

	def retain_dropped_item_message(self, location, local_item_list, native_item, native_item_2 = None):
		for current_item in local_item_list:
			if (current_item not in [native_item, native_item_2]):
				self.update_arrival_item_info(location, current_item)					# Keeping dropped-item-text on releveant location.

	def update_tree_message(self):
		self.arrival_info[self.tree_location] = self.tree_message_updated				# Update tree message when necessary (after grabbing arrows).
		
	def update_supplies_message(self, first_interaction):
		if (first_interaction):															# If first interaction with the supplies.
			self.arrival_info[self.supplies_location] = self.supplies_message_01		# Update to the first new message for this location.
		
		else:																			# If second interaction with the supplies.
			self.arrival_info[self.supplies_location] = self.supplies_message_02		# Update to the second new message for this location.
			
	def update_door_message(self, first_interaction):
		if (first_interaction):															# If first interaction with the door.
			self.arrival_info[self.door_location] = self.door_message_01				# Update to the first new message for this location.
		
		else:																			# If second interaction with the door.
			self.arrival_info[self.door_location] = self.door_message_02				# Update to the second new message for this location.
			
	def update_venom_message(self):
		print "Hei"
		


class Commands:
	def __init__(self):
		self.help_cmds = ["view help", "show help", "need help", "help"]							# Allowed commands for showing help.
		self.location_cmds = ["view location", "show location", "location", "info"]					# Allowed commands for info on location.
		self.inventory_cmds = ["view inventory", "show inventory", "inventory", "i"]				# Allowed commands for showing inventory.
		self.first_cmd_move = ["go", "walk", "move", "run", "relocate", "hike"]						# Allowed first commands for moving in world.
		self.first_cmd_grab = ["grab", "take", "get", "aquire", "pick", "obtain"]					# Allowed first commands for grabbing items.
		self.first_cmd_drop = ["drop", "loose", "leave", "discard", "neglect"]						# Allowed first commands for dropping items.
		self.first_cmd_climb = ["climb", "mount", "peak", "reach"]									# Allowed first commands for climbing objects.
		self.first_cmd_remove = ["rearrange", "remove", "relocate"]									# Allowed first commands rearranging supplies.
		self.first_cmd_door = ["explode", "blast", "destroy", "detonate", "place", "arm", "break"]	# Allowed first commands destroying the door.
		self.first_cmd_inject = ["inject", "apply", "drain"]										# Allowed first commands for applying antidote.
		self.climbable_objects = ["tree", "cliff"]													# Allowed commands for climbable objects.
		self.climb_down_cmd = ["down"]																# Allowed commands for climbiung down.
		self.removable_objects = ["supplies", "merchandise", "scrap"]								# Allowed commands for the supplies.
		self.destructibal_objects = ["door", "entrance", "gate"]									# Allowed commands for the door.
		self.use_terminal_cmds = ["enter mou", "enter supercomputer", "access mou", "access supercomputer",
			"enter console", "access console", "enter terminal", "access terminal", "use terminal"]	# Allowed commands for using the terminal.
		self.MOU_cmds = ["access MOU commands", "load file AA_file.nc", "enable scripting for AA_file.nc", "set script type to NevCee",
			"upon||AA_file.nc||enter||<0> -> delete_line(<714>)", "upon||AA_file.nc||enter||<1> -> go_to_line(<714>)",
			"upon||AA_file.nc||OneLineWrite -> exit(AA_file.nc)", "enter(AA_file.nc)", "OneLineWrite('AA_defense.enabled = FALSE')", "exit MOU"]
		self.directions = {"north": (-1, 0), "east":  (0, 1), "south": (1, 0), "west":  (0, -1)}	# Coordinate change related to direction.
		self.exit_cmds = ["exit game", "end game", "stop game", "exit", "end", "stop"]		# Allowed commands for exiting the game and returning to cmd.

	# Function that displays help on allowed commands.
	def show_help(self):
		print "\nHELP MENU\n\n(1) IN-GAME INFO"
		print "------------------------------------------------------------------------"
		print "Use one of these commands for showing info about current location:"
		for lc_cmd in self.location_cmds:
			print lc_cmd, "|",
		print "\n\nTo see your inventory use either of these commands:"
		for inv_cmd in self.inventory_cmds:
			print inv_cmd, "|",
		
		print "\n\n\n(2) MOVEMENT"
		print "------------------------------------------------------------------------"
		print "Allowed commands for directons to move:"
		for direction in self.directions.keys():
			print direction, "|",
		print "\n\nAllowed verbs in combination with the directions:"
		for move_verb in self.first_cmd_move:
			print move_verb, "|",
		
		print "\n\n\n(3) OBTAINING AND DISCARDING ITEMS"
		print "------------------------------------------------------------------------"
		print "Allowed verbs to use when obtaining items from the environment:"
		for obtain_verb in self.first_cmd_grab:
			print obtain_verb, "|",
		print "\n\nAllowed verbs to use for discarding items in your inventory:"
		for discard_verb in self.first_cmd_drop:
			print discard_verb, "|",

		print "\n\n\n(4) OTHER INTERACTION WITH THE WORLD"
		print "------------------------------------------------------------------------"
		print "Throughout the game you will encounter situations where interacting"
		print "with the world to do location specific moves or similar is needed."
		print "Depending on the situation you are in; here are the allowed verb commands:\n"
		for climb_verb in self.first_cmd_climb:
			print climb_verb, "|",
		print "\n"
		for detonate_verb in self.first_cmd_grenade:
			print detonate_verb, "|",
		print "\n"
		for inject_verb in self.first_cmd_inject:
			print inject_verb, "|",

		print "\n\n\n(4) EXITING THE GAME"
		print "------------------------------------------------------------------------"
		print "Below are the commands for exiting the game at any time you wish to do so:"
		for exit_cmd in self.exit_cmds:
			print exit_cmd, "|",
		print "\n"


# Function that is the actual game (using instances of classes above).
def game(cmds, world, messages, items):
	os.system("cls")					# Clear command prompt before game starts.
	print messages.welcome				# Print the game info/welcome messasge.

	game_over = False					# Initially sets game over to false.
	num_visits_plants = 0				# Initially 0 visits to the poisionis plant.
	items.assign_empty_items_arrays()	# Initially empty, bu to be filled when e.g. item dropped.
	items.add_items_to_world()			# Fill world with story required items to be picked up.

	user_name = "\n" + raw_input("Who's playing?\n") + "--: "	# Enter name of player (to be prompt for rest of game).
	user_cmd = "sample string to be changed inside while loop"	# Declare variable so first "if" inside while-loop works.
	cmd_words = user_cmd.split()								# Declare variable so first "if" inside while-loop works.
	print "\n"

	items.inventory.append("rope")
	items.inventory.append("hook")

	# Main loop that iterates once per user command. Terminates upon game_over = True (death) or game comletion.
	while (True):

		# If player is stung last iteration.
		if (world.has_been_stung == True):

			# If this iters are 2 after sting.
			if (world.iters_num_after_sting == 1):
				print messages.death_venom			# Display death message for venom.
				game_over = True 					# Set game_over to True in this case.

			else:
				world.iters_num_after_sting = 1

		# If player died in the previous iteration.
		if (game_over == True):
			print "\nGame over!\nTry again and don't make the same mistake next time."
			break

		# If the player moved in the previous iteration.
		if (world.has_moved == True):
			messages.display_arrival_message((world.c_row, world.c_col))		# Display arrival info for new location.
			world.has_moved = False 											# Reset world.has_moved to False before new command.
		
		user_cmd = raw_input(user_name).lower()		# Each iteration the player enters a command.
		cmd_words = user_cmd.split()				# Array of words that make up the command from player.
		#print [item for sublist in items.attainable_items.values() for item in sublist if len(sublist) > 0]
		#att = [[item_location, item] for item_location, item in items.attainable_items.iteritems() if len(item) > 0]
		#print att

		# If any command is provided at all.
		if (len(cmd_words) > 0):

			# If the commands is made up of two words and doesn't conflict with the four elif's further down.
			if ((len(cmd_words) == 2) and (user_cmd not in cmds.inventory_cmds) and (user_cmd not in cmds.location_cmds)
				and (user_cmd not in cmds.help_cmds) and (user_cmd not in cmds.use_terminal_cmds) and (user_cmd not in cmds.exit_cmds)):

				# -------- SECTION THAT HANDLES MOVEMENT --------.
				if ((cmd_words[0] in cmds.first_cmd_move)):
					user_cmd = user_cmd.replace(cmd_words[0], cmds.first_cmd_move[0])		# Replace first word with "go" to simplify.
					
					# If user suggests an allowed direction.
					if (cmd_words[1] in cmds.directions.keys()):
						next_row = world.c_row + cmds.directions[cmd_words[1]][0]			# Find row for where user wants to go.
						next_column = world.c_col + cmds.directions[cmd_words[1]][1]		# Find column for where user wants to go.
						
						# If there is no obstacles where the player wants to go and if the player is not in the tree.
						if ((world.map[next_row][next_column] == 0) and ((world.c_row, world.c_col) != world.tree_location)):
							world.map[world.c_row][world.c_col] = 0 						# The location from which the player moved is set to 0.		
							world.c_row = next_row											# Update world.c_row to be the new row the user moved to.
							world.c_col = next_column										# Update world.c_col to be the new column the user moved to.
							world.map[next_row][next_column] = world.player_indicator		# Update the position of the player indicator on the map.
							world.has_moved = True											# Make sure the next iteration knows the user moved this iters.
							world.view_map()												# Display map of world. Mostly for developing purposes.

							# If player arrives at venom location for the first time (has then not used antidote because would be dead).
							if (((world.c_row, world.c_col) == world.venom_location) and (world.has_injected_antidote == False)):
								world.has_been_stung = True 							# Set that pleyer now has been stung by venomous plant.
								world.iters_num_after_sting = 0 						# This is the same iteration as the plant sting occurs.

						# If user tries to move in a direction where she/he will be killed.	
						elif ((next_row, next_column) in world.death_locations):
							messages.display_death_message((next_row, next_column))		# Display death message on relevant death location.
							game_over = True											# Make sure next iteration knows the user died in this iteration.
			
						else:
							print "\nYou cant go that way"

					else:
						print "%s is not a valid direction!" % (cmd_words[1])


				# -------- SECTION THAT HANDLES GRABBING ITEMS --------.
				elif (cmd_words[0] in cmds.first_cmd_grab):
					loop_counter = 0
					for item_location, item_array in items.attainable_items.iteritems():
						if (cmd_words[1] in item_array):

							# If the player is at the same place as the item.
							if ((world.c_row, world.c_col) == item_location):

								# Checking if inventory is full.
								if (len(items.inventory) < items.inventory_capacity):

									# If player is trying to access the antidote.
									if ((item_location == world.supplies_location) and (cmd_words[1] == "antidote")):

										# If player tries to grab antidote after supplies have been moved.
										if (world.has_removed_supplies == True):
											items.add_item(cmd_words[1], item_location)					# Adding antidote to inventory.
											messages.update_supplies_message(first_interaction = False)	# Updating supplies message second time.
											messages.retain_dropped_item_message(item_location, items.attainable_items[item_location], "antidote")
											print "Grabbed %s" % (cmd_words[1])							# Informing that antidote is grabbed.


										else:
											print "You can't reach the antidote; there's too much supplies blocking the way. Try to remove it."

									# If player is trying to access the door.
									elif ((item_location == world.door_location) and (cmd_words[1] == "rope")):

										# If player tries to grab rope after door is exploded.
										if (world.has_destroyed_door == True):
											items.add_item(cmd_words[1], item_location)					# Adding rope to inventory.
											messages.update_door_message(first_interaction = False)		# Updating door message second time.
											messages.retain_dropped_item_message(item_location, items.attainable_items[item_location], "rope")
											print "Grabbed %s" % (cmd_words[1])							# Informing that rope is grabbed.

										else:
											print "There's a door blocking your way. Try to destroy it."

									# If the player grabs hook or grenade from the hook/grenade location.
									elif ((item_location == world.hook_grenade_location) and (cmd_words[1] in ["hook", "grenade"])):
										items.add_item(cmd_words[1], item_location)							# Adding hook/grenade to inventory.
										messages.arrival_info[item_location] = messages.hook_message_01		# Updating message after grabbing.
										messages.retain_dropped_item_message(item_location, items.attainable_items[item_location], "hook", "grenade")
										print "Grabbed %s" % (cmd_words[1])									# Informing that hook/grenade is grabbed.

									else:
										items.add_item(cmd_words[1], item_location)			# Adding grabbed item to inventory.
										print "Grabbed %s" % (cmd_words[1])					# Informing player that item is grabbed.

										
									# Updating arrival info in tree after grabbing arrows.
									if (item_location == world.tree_location):
										messages.update_tree_message()
									
									# Removing last part of arrival info when grabbing items if item has earlier been dropped here.
									if (messages.new_item_at_location + cmd_words[1] + "." in messages.arrival_info[item_location]):
										messages.remove_relevant_sentence(cmd_words[1], item_location)
										
										
								else:
									print "Your inventory is full. You cannot carry any more items."
									break
										
							else:
								print "There is no %s at this location." % (cmd_words[1])
								break
								
							break
									
						elif (cmd_words[1] in items.inventory):
							print "You already have the %s" % (cmd_words[1])
							break
							
						loop_counter += 1

					# If looped through all locations, then no such item (cmd_words[1]) exists.
					if (loop_counter == world.num_locations):
						print "%s is no valid item in 'Escape'." % (cmd_words[1])
							

				# -------- SECTION THAT HANDLES DROPPING ITEMS --------.
				elif (cmd_words[0] in cmds.first_cmd_drop):
					if (cmd_words[1] in items.inventory):
							print "Dropped %s" % (cmd_words[1])
							items.remove_item(cmd_words[1], (world.c_row, world.c_col))
							messages.update_arrival_item_info((world.c_row, world.c_col), cmd_words[1])

					else:
						loop_counter = 0
						for item_array in items.attainable_items.values():
							if (cmd_words[1] in item_array):
								print "You dont have the %s." % (cmd_words[1])
								break
								
							loop_counter += 1
						
						if (loop_counter == world.num_locations):
							print "%s is no valid item in 'Escape'." % (cmd_words[1])
				
				# -------- SECTION THAT HANDLES CLIMBING OBJECTS --------.
				elif (cmd_words[0] in cmds.first_cmd_climb):

					# If player wants to climb an object which is climbable.
					if (cmd_words[1] in cmds.climbable_objects):

						# If player is located at the east side of the tree.
						if ((cmd_words[1] == "tree") and ((world.c_row, world.c_col) == world.climb_tree_location)):
							world.map[world.c_row][world.c_col] = 0 							# Set climbable location to 0 when climbing.
							world.c_row = world.tree_location[0]								# Change player coordinates to the tree coord.
							world.c_col = world.tree_location[1]								# Change player coordinates to the tree coord.
							world.map[world.c_row][world.c_col] = world.player_indicator		# Indicate, on the map, that player is in tree.
							world.view_map()													# View map for development purposes.
							messages.display_arrival_message((world.c_row, world.c_col))		# Display arrival message in tree.

						# If player is located at the bottom (south of) of the cliff.
						elif ((cmd_words[1] == "cliff") and ((world.c_row, world.c_col) == world.climb_cliff_location)):

							# If player 
							if (("rope" in items.inventory) and ("hook" in items.inventory)):
								world.map[world.c_row][world.c_col] = 0 							# Set climbable location to 0 when climbing.
								world.c_row = world.cliff_location[0]								# Change player coordinates to the tree coord.
								world.c_col = world.cliff_location[1]								# Change player coordinates to the tree coord.
								world.map[world.c_row][world.c_col] = world.player_indicator		# Indicate, on the map, that player is in tree.
								world.view_map()													# View map for development purposes.
								messages.display_arrival_message((world.c_row, world.c_col))		# Display arrival message in tree.

							else:
								print("You must have both the rope and the hook in order to make this climb\n\nYour current inventory is:")
								items.view_inventory()



						# If player tries to climb further while being at the top of the tree.
						elif ((cmd_words[1] == "tree") and ((world.c_row, world.c_col) == world.tree_location)):
							print "You're already at the top of the tree. 'climb down' if you want to get down."

						# If player tries to climb further while being at the top of the cliff.
						elif ((cmd_words[1] == "cliff") and ((world.c_row, world.c_col) == world.cliff_location)):
							print "You're already at the top of the cliff. 'climb down' if you want to get down."

							
						else:
							print "There is no climbable %s from this location" % (cmd_words[1])

					# If player wants to climb down from the tree or cliff.
					elif (cmd_words[1] in cmds.climb_down_cmd):

						# If player wants to climb down from the tree.
						if ((world.c_row, world.c_col) == world.tree_location):
							world.map[world.c_row][world.c_col] = 1 						# Reset tree to value 1 on the map.
							world.c_row = world.c_row										# When climbing down, the row stays the same.
							world.c_col = world.c_col - 1 									# When climbing down, column shifts to the left.
							messages.display_arrival_message((world.c_row, world.c_col))	# Display arrival message when coming down from tree.

						# If player wants to climb down from the tree.
						if ((world.c_row, world.c_col) == world.cliff_location):
							world.map[world.c_row][world.c_col] = 1 						# Reset tree to value 1 on the map.
							world.c_row = world.c_row + 1									# When climbing down, the row stays the same.
							world.c_col = world.c_col 										# When climbing down, column shifts to the left.
							messages.display_arrival_message((world.c_row, world.c_col))	# Display arrival message when coming down from tree.

						else:
							print "You can't climb down from here"

					else:
						print "%s is no climbable object in 'Escape'" % (cmd_words[1])
						
				# -------- SECTION THAT HANDLES MOVING SUPPLIES FOR ANTIDOTE --------.
				elif (cmd_words[0] in cmds.first_cmd_remove):	

					# If the player tries to move a valid moveable object.
					if (cmd_words[1] in cmds.removable_objects):

						# If the player is at the same location as the supplies.
						if ((world.c_row, world.c_col) == world.supplies_location):
							messages.update_supplies_message(first_interaction = True)		# Update arrival info for the first time.
							messages.retain_dropped_item_message(world.supplies_location, items.attainable_items[world.supplies_location], "antidote")
							messages.display_arrival_message(world.supplies_location)		# Display the newly updated arrival info.
							world.has_removed_supplies = True 								# The supplies has now been removed.
							
						else:
							print "There is no removeable %s from this location" % (cmd_words[1])
						
					else:
						print "%s are no valid removeable objects in 'Escape'" % (cmd_words[1])
						
				# -------- SECTION THAT HANDLES BLASTING THE DOOR BLOCKING THE ROPE --------.
				elif (cmd_words[0] in cmds.first_cmd_door):

					# If player tries to blow up a valid word for "door".
					if (cmd_words[1] in cmds.destructibal_objects):

						# If the player posesses the grenade for destroying the door.
						if ("grenade" in items.inventory):

							# If the player is at the same location as the door.
							if ((world.c_row, world.c_col) == world.door_location):
								messages.update_door_message(first_interaction = True)			# Update arrival info for the first time.
								messages.retain_dropped_item_message(world.supplies_location, items.attainable_items[world.supplies_location], "antidote")
								messages.display_arrival_message((world.c_row, world.c_col))	# Display the newly updated arrival info.
								items.inventory.remove("grenade")								# Remove grenade from inventory after use.
								world.has_destroyed_door = True 								# The door has now been destroyed.
								
							else:
								print "There is no destructible %s at this location" % (cmd_words[1])

						else:
							print "You don't have an explosive."
						
					else:
						print "%s are no valid destructible objects in 'Escape'" % (cmd_words[1])

				# -------- SECTION THAT HANDLES PLAYER INJECTING ANTIDOTE --------.
				elif (cmd_words[0] in cmds.first_cmd_inject):
					
					# If player provides valid command for antidote.
					if (cmd_words[1] == "antidote"):
						cmd_words[0] = cmds.first_cmd_inject[0]				# To simplify for death check on next iteration.

						# If player has antidote in inventory.
						if ("antidote" in items.inventory):
							if (world.has_been_stung == True):
								world.has_injected_antidote = True 		# Indicate that the antidote has been injected.
								world.has_been_stung = False 			# Indicate that the antidote has been injected.
								items.inventory.remove("antidote")		# Remove antidote from inventory after injection.
								messages.arrival_info[world.venom_location] = messages.venom_message_01		# Update info.
								print messages.successfull_injection	# Inform player of the successfull antidote injection.
								print "\n" + messages.arrival_info[world.venom_location]

							else:
								print messages.death_antidote				# Display death message from taking antidote without venom.
								game_over = True 							# Game over when player dies from antidote overdose.
						else:
							print "You don't have the antidote."

					else:
						print "%s is no injectable item in 'Escape'." % (cmd_words[1])

				else:
					print "I don't understand the command: %s" % (user_cmd)

			# -------- SECTION THAT HANDLES PLAYER INTERACTION WITH THE MOU --------.
			elif (user_cmd in cmds.use_terminal_cmds):

				# If player is at the MOU location when accessing it.
				if ((world.c_row, world.c_col) == world.MOU_location):
					print messages.MOU_feedback_01								# Print welcome-to-MOU message.

					# Loop over all commands in the MOU-interaction-sequence.
					for i in xrange(0, len(cmds.MOU_cmds)):
						current_command = raw_input(messages.MOU_prompts[i])	# Current command from player.

						while ((current_command != cmds.MOU_cmds[i]) and (current_command != "exit")):
							print "\n-------------------------------------------"
							print "INVALID MOU-COMMAND OR COMMAND OUT OF ORDER"
							print "---------------------------------------------\n"

							current_command = raw_input(messages.MOU_prompts[i])	# Current command from player.

						# If current_command is the correct one.
						if (current_command == cmds.MOU_cmds[3]):
							print messages.MOU_feedback_02					# Give feedback for enabling NevCee script.

						elif (current_command == cmds.MOU_cmds[7]):
							print messages.MOU_feedback_03					# Give feedback for entering console.

						elif (current_command == cmds.MOU_cmds[8]):
							print messages.MOU_feedback_04					# Give feedback for exiting AA_file.nc.

						elif ((current_command == cmds.MOU_cmds[9]) or (current_command == "exit" and i == 9)):
							world.has_disabled_AA = True
							print messages.MOU_feedback_05					# Give feedback for exiting MOU.

						elif (current_command == "exit"):
							print "\n--------------\nNO CHANGES MADE.\nEXITING MOU...\n--------------"
							break

				else:
					print "There's no Military Operating Unit at this location."

			# If user wants to see info about current location.
			elif (user_cmd in cmds.location_cmds):
				messages.display_arrival_message((world.c_row, world.c_col))

			# If user wants to see current inventory.
			elif (user_cmd in cmds.inventory_cmds):
				items.view_inventory()

			# If user wants to see help.
			elif (user_cmd in cmds.help_cmds):
				cmds.show_help()

			elif (user_cmd in cmds.exit_cmds):
				print "Exiting game..."
				break

			else:
				print "I don't understand the command: %s" % (user_cmd)
		
		else:
			print "Provide a command to do something!"



if (__name__ == "__main__"):
	world_object = Map()			# Map object that stores locations in the world and gives acces to printing the map.
	inventory_object = Items()		# Items object that stores inventory and gives access to various inventory functions.
	cmds_object = Commands()		# Commands object that stores all allowed commands and gives acces to display help function.
	message_object = Messages()		# Messages object that stores messages for e.g. locations and gives access to message chaning functions.

	# Calling game function and thus starts the game. Input arguments are the objects created just above.
	game(cmds_object, world_object, message_object, inventory_object)
