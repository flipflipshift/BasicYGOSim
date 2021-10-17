#Yugioh probability estimator that takes Prosperity, Desires, Upstart, Extravagance, Duality into account
#Very early stages of testing

#deck_size and hand_size are self-explanatory
#In input_cards_here: Enter card name *space* quantity, then hit enter. Leave no spaces in card names
#Certain draw cards have their effects built in. Write Desires, Prosperity, Extravagance, Upstart as the names for those cards

#For input_possibilities_heare, list the acceptable combinations of cards in hand. Follow the syntax in the example
#In the example here, the first line means "1 or more Bond, 1 or more Bridge, exactly 0 Garnet and 1 or fewer Carbuncle"
#Each line represents a different acceptable combination of cards in hand

#Final line is the number of trials

#outputs the estimated probability you get one of these desired combinations
deck_size = 40
hand_size = 5
input_cards_here="""
Beacon 3
Bond 3
Bridge 3
Prosperity 3
Upstart 1
Carbuncle 2
Garnet 1
"""
input_possibilities_here="""
1 + Bond AND 1 + Bridge AND 0 = Garnet AND 1 - Carbuncle
1 + Bond AND 1 + Beacon AND 0 = Garnet AND 1 - Carbuncle
1 + Bridge AND 1 + Beacon AND 0 = Garnet AND 1 - Carbuncle
2 + Bridge AND 0 = Garnet AND 1 - Carbuncle
"""
num_trials=10000

#Below is the actual code; can ignore



import random

def empty_deck(n):
	deck=[]
	for i in range(0, n):
		deck.append("blank")
	return deck


def add_card(deck, name, quantity):
	for i in range(0, quantity):
		del deck[0]
		deck.append(name)
	return deck

def get_hand(deck, k):
	m=min(len(deck),k+9)
	for i in range(0,m):
		rand=random.randint(i,len(deck)-1)
		temp=deck[rand]
		deck[rand]=deck[i]
		deck[i]=temp
	hand=[]
	extras=[]
	for i in range(0,k):
		hand.append(deck[i])
	for i in range(k,m):
		extras.append(deck[i])
	return([hand,extras])

def is_valid(hand, condition):
	for cond in condition:
		card=cond[0]
		sign=cond[2]
		num=0
		for c in hand:
			if c==card:
				num+=1
		if num<cond[1] and sign!="-":
			return False
		if num>cond[1] and sign!="+":
			return False
	return True

def is_one_valid(hand,possibilities):
	for p in possibilities:
		if is_valid(hand,p):
			return True
	return False

def is_one_valid_draw(hand,extras,possibilities,can_extrav,can_desires,can_upstart,can_prosperity,can_duality):
	if is_one_valid(hand,possibilities):
		return True
	if can_desires and "Desires" in hand:
		temp_hand=hand.copy()
		temp_extras=extras.copy()
		temp_hand.append(temp_extras.pop())
		temp_hand.append(temp_extras.pop())
		if is_one_valid_draw(temp_hand,temp_extras,possibilities,False,False,can_upstart,False,can_duality):
			return True
	if can_extrav and "Extravagance" in hand:
		temp_hand=hand.copy()
		temp_extras=extras.copy()
		temp_hand.append(temp_extras.pop())
		temp_hand.append(temp_extras.pop())
		if is_one_valid_draw(temp_hand,temp_extras,possibilities,False,False,False,False,can_duality):
			return True
	if can_prosperity and "Prosperity" in hand:
		for i in range(0,6):
			temp_hand=hand.copy()
			temp_extras=extras.copy()
			temp_hand.append(temp_extras[i])
			del temp_extras[0:6]
			if is_one_valid_draw(temp_hand,temp_extras,possibilities,False,False,False,False,can_duality):
				return True
	if can_upstart and "Upstart" in hand:
		temp_hand=hand.copy()
		temp_extras=extras.copy()
		temp_hand.append(extras.pop(0))
		temp_hand.remove("Upstart")
		if is_one_valid_draw(temp_hand,temp_extras,possibilities,False,can_desires,can_upstart,False,can_duality):
			return True
	if can_duality and "Duality" in hand:
		for i in range(0,3):
			temp_hand=hand.copy()
			temp_extras=extras.copy()
			temp_hand.append(temp_extras[i])
			del temp_extras[0:3]
			if is_one_valid_draw(temp_hand,temp_extras,possibilities,False,can_desires,can_upstart,can_prosperity,False):
				return True
	return False

deck=empty_deck(deck_size)
cards=input_cards_here.splitlines()
cards.pop(0)
for card in cards:
	s=card.split(" ")
	deck=add_card(deck,s[0],int(s[1]))

possibilities=[]
text_possibilities=input_possibilities_here.splitlines()
text_possibilities.pop(0)
for possibility in text_possibilities:
	conditions=[]
	text_conditions=possibility.split(" AND ")
	for condition in text_conditions:
		parts=condition.split(" ")
		conditions.append([parts[2],int(parts[0]),parts[1]])
	possibilities.append(conditions)

counter=0
for i in range(0,num_trials):
	hand=get_hand(deck,hand_size)
	if is_one_valid_draw(hand[0],hand[1],possibilities,True,True,True,True,True):
		counter+=1
print("probability of success: "+ str(counter/num_trials*100)+"%")

