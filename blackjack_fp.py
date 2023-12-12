import pygame
import random
import copy
from pygame.locals import *

pygame.init()

cards = ["2", "3", "4", "5","6", "7", "8", "9", "10", "J", "Q", "K", "A"]
deck = 4 * cards

HEIGHT = 450
WIDTH = 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Blackjack")
fps = 60
timer = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 45)
small_font = pygame.font.SysFont("Arial", 20)
med_font = pygame.font.SysFont("Arial", 30)
color = pygame.Color(138, 73, 36)
active = False
hand_active = False

record = [0, 0, 0]
player_score = 0
dealer_score = 0
results = ["","YOU BUSTED", "YOU WIN", "DEALER WINS", "TIE GAME"]

initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
add_score = False


def draw_game(act, record, result):
    button_list = []

    if not act:
        deal = pygame.draw.rect(screen, "white", [150, 185, 300, 75], 0, 5)
        pygame.draw.rect(screen, "black", [150, 185, 300, 75], 3, 5)
        deal_text = font.render("DEAL HAND", True, "black")
        screen.blit((deal_text), (195, 197.5))
        button_list.append(deal)
    else:
        hit = pygame.draw.rect(screen, "white", [65, 350, 200, 75], 0, 5)
        pygame.draw.rect(screen, "black", [65, 350, 200, 75], 3, 5)
        hit_text = font.render("HIT", True, "black")
        screen.blit((hit_text), (135, 362.5))
        button_list.append(hit)

        stand = pygame.draw.rect(screen, "white", [335, 350, 200, 75], 0, 5)
        pygame.draw.rect(screen, "black", [335, 350, 200, 75], 3, 5)
        stand_text = font.render("STAND", True, "black")
        screen.blit((stand_text), (375, 362.5))
        button_list.append(stand)

        score_text = small_font.render(f"Wins: {record[0]}   Losses: {record[1]}   Draws: {record[2]}", True, "white")
        screen.blit((score_text), (10, 5))

    if result != 0:
        screen.blit(font.render(results[result], True, "white"), (325, 0))
        deal = pygame.draw.rect(screen, "white", [200, 55, 225, 75], 0, 5)
        pygame.draw.rect(screen, "black", [200, 55, 225, 75], 3, 5)
        deal_text = font.render("NEW HAND", True, "black")
        screen.blit((deal_text), (210, 65))
        button_list.append(deal)
        
    return button_list


def deal_cards(current_hand, current_deck):
    card = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    return current_hand, current_deck

def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, "white", [50 + (50*i), 220 - (20*i), 80, 120], 0, 5)
        screen.blit(font.render(player[i], True, 'black'), (55 + 50 * i, 220 - 20 * i))
        pygame.draw.rect(screen, "red", [50 + (50 * i), 220 - (20 * i), 80, 120], 3, 5)

    for i in range(len(dealer)):
        pygame.draw.rect(screen, "white", [325 + (50*i), 220 - (20*i), 80, 120], 0, 5)
        if i != 0 or reveal:
            screen.blit(font.render(dealer[i], True, 'black'), (330 + (50*i), 220 - (20*i), 80, 120))
        else:
            screen.blit(font.render("?", True, 'black'), (330 + (50*i), 220 - (20*i), 80, 120))
        pygame.draw.rect(screen, "blue", [325 + (50 * i), 220 - (20 * i), 80, 120], 3, 5)


def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count("A")
    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])

        if hand[i] in ["10", "J", "Q", "K"]:
            hand_score += 10

        elif hand[i] == "A":
            hand_score += 11

    if hand_score > 21 and aces_count > 0:
        for i in range(aces_count):
            if hand_score > 21:
                hand_score -= 10

    return hand_score

def draw_scores(player, dealer):
    screen.blit(med_font.render(f"Your Score: {player}", True, "white"), (5, 35))
    if reveal_dealer:
        screen.blit(med_font.render(f"Dealer Score: {dealer}", True, "white"), (5, 75))

def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    if not hand_act and deal_score >= 17:
        if play_score > 21:
            result = 1
        elif deal_score < play_score <= 21 or deal_score > 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4

        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1

            add = False

    return result, totals, add
            
            
            


run = True
while run:

    timer.tick(fps)
    screen.fill(color)
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False


    if active:
        player_score = calculate_score(my_hand)
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)
    
    buttons = draw_game(active, record, outcome)


    #For Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    reveal_dealer = False
                    add_score = True
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                   my_hand, game_deck = deal_cards(my_hand, game_deck)
                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        add_score = True
                        player_score = 0
                        dealer_score = 0
                        

    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, record, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, record, add_score)

    pygame.display.flip()


pygame.quit()
