from random import randint


def handler(event, context):
    take = ['клад', 'положи', 'класть', 'полож']
    pullist = ['беру', 'тяну', 'гребу', 'потяну']
    # if event['request']['nlu']['tokens'][-1][-1] == '.':
    # event['request']['nlu']['tokens'][-1] = event['request']['nlu']['tokens'][:-1]
    if 'session' in event and 'new' in event['session'] and event['session']['new']:
        text = 'Привет! Я - Соня, в этом навыке ты сможешь поиграть со мной в UNO. Хочешь начать игру, или узнать ' \
               'правила?'
        tts = text
        stage = 1
        stage_2 = 0

    if len(event['request']['nlu']['tokens']) > 0 and stage == 1 and stage_2 == 0:
        choice = 0
        user_cards = []
        skill_cards = []
        rules = ['правила', 'как', 'объясни', 'непонятно']
        game = ['играть', 'игра', 'запускай', 'включай', 'поиграть', 'включи', 'запусти']
        for i in event['request']['nlu']['tokens']:
            for j in game:
                if i.lower() in j:
                    choice = 'game'
            for k in rules:
                if i.lower() in k:
                    choice = 'rules'
        if choice == 0:
            text = 'Извините, не понятно'
            tts = text
        if choice == 'game':
            deck = ['0 красный', '0 жёлтый', '0 зелёный', '0 синий', '1 красный', '1 жёлтый', '1 зелёный',
                    '1 синий', '1 красный', '1 жёлтый', '1 зелёный', '1 синий', '2 красный', '2 жёлтый',
                    '2 зелёный', '2 синий', '2 красный', '2 жёлтый', '2 зелёный', '2 синий', '3 красный',
                    '3 жёлтый', '3 зелёный', '3 синий', '3 красный', '3 жёлтый', '3 зелёный', '3 синий',
                    '4 красный', '4 жёлтый', '4 зелёный', '4 синий', '4 красный', '4 жёлтый', '4 зелёный',
                    '4 синий', '5 красный', '5 жёлтый', '5 зелёный', '5 синий', '5 красный', '5 жёлтый',
                    '5 зелёный', '5 синий', '6 красный', '6 жёлтый', '6 зелёный', '6 синий', '6 красный',
                    '6 жёлтый', '6 зелёный', '6 синий', '7 красный', '7 жёлтый', '7 зелёный', '7 синий',
                    '7 красный', '7 жёлтый', '7 зелёный', '7 синий', '8 красный', '8 жёлтый', '8 зелёный',
                    '8 синий', '8 красный', '8 жёлтый', '8 зелёный', '8 синий', '9 красный', '9 жёлтый',
                    '9 зелёный', '9 синий', '9 красный', '9 жёлтый', '9 зелёный', '9 синий', '+2 красный',
                    '+2 жёлтый', '+2 зелёный', '+2 синий', '+2 красный', '+2 жёлтый', '+2 зелёный',
                    '+2 синий', 'пропуск красный', 'пропуск красный', 'пропуск жёлтый', 'пропуск жёлтый',
                    'пропуск зелёный', 'пропуск зелёный', 'пропуск синий', 'пропуск синий', 'смена цвета',
                    'смена цвета', 'смена цвета', 'смена цвета', '+4 смена цвета', '+4 смена цвета',
                    '+4 смена цвета', '+4 смена цвета']
            x = 0
            while x == 0:
                face_card = deck.pop(randint(0, len(deck)))
                for i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                    if face_card[0] == i:
                        x = 1
            for i in range(7):
                user_cards.append(deck.pop(randint(0, len(deck))))
                skill_cards.append(deck.pop(randint(0, len(deck))))
            bamp = check_user(face_card, user_cards)
            text = 'Хорошо, первым ходишь ты, вот твоя колода: ' + ' '.join(
                user_cards) + ' Верхняяя карта: ' + face_card + '. '
            if bamp[1] == 0:
                text += bamp[0]
                tts = text
                stage = 3
                stage_2 = 3
            if len(bamp[1]) == 1 and bamp[1] != 0:
                text += 'ты можешь положить только ' + bamp[1][0] + '. Положишь, или потянешь?'
                stage = 3
                stage_2 = 2
                one_card = bamp[1][0]
                can_take = bamp[1]
            if len(bamp[1]) > 1 and len(bamp[1]) < len(user_cards):
                text += bamp[0] + ', '.join(bamp[1]) + '. Положишь, или потянешь?'
                stage = 4
                stage_2 = 4
                can_take = bamp[1]
            if len(bamp[1]) == len(user_cards):
                text += bamp[0] + '. Положишь, или потянешь?'
                stage = 4
                stage_2 = 4
                can_take = bamp[1]
            tts = text
            stage_2 = 1
        elif choice == 'rules':
            text = 'Правила'
            tts = text

    if len(event['request']['nlu']['tokens']) > 0 and stage == 3 and stage_2 == 3:
        z = 0
        for i in event['request']['nlu']['tokens']:
            for j in pullist:
                if i.lower() in j or j in i.lower():
                    z += 1
        if z > 0:
            if len(deck) > 0:
                list_pull = pull(deck)
                user_cards.append(list_pull[0])
                deck = list_pull[1]
                if list_pull[0].split()[0] == face_card.split()[0] or list_pull[0].split()[-1] == face_card.split()[
                    -1] or list_pull[0].split()[-1] == 'цвета':
                    text = 'Ты можешь положить взятую тобою карту - ' + list_pull[0]
                    tts = text
                    stage = 3
                    stage_2 = 2
                    one_card = list_pull[0]
                    can_take = [list_pull[0]]
                else:
                    text = ''
                    tts = text
            else:
                text = 'В колоде кончились карты'
                tts = text
                stage = 8
                stage_2 = 8

    if len(event['request']['nlu']['tokens']) > 0 and stage == 3 and stage_2 == 2:
        for i in event['request']['nlu']['tokens']:
            for k in take:
                if i.lower() in k or k in i.lower():
                    face_card = user_cards.pop(user_cards.index(one_card))
                    stage = 8
                    stage_2 = 8
            z = 0
            for j in pullist:
                if i.lower() in j:
                    z += 1
            if z > 0:
                if len(deck) > 0:
                    list_pull = pull(deck)
                    user_cards.append(list_pull[0])
                    deck = list_pull[1]
                    if list_pull[0].split()[0] == face_card.split()[0] or list_pull[0].split()[-1] == face_card.split()[
                        -1] or list_pull[0].split()[-1] == 'цвета':
                        text = 'Ты можешь положить взятую тобою карту - ' + list_pull[0]
                        tts = text
                        stage = 4
                        stage_2 = 4
                        can_take.append(list_pull[0])

    if len(event['request']['nlu']['tokens']) > 0 and stage == 4 and stage_2 == 4:
        for k in take:
            if event['request']['nlu']['tokens'][0] in k or k in event['request']['nlu']['tokens'][0]:
                if event['request']['nlu']['tokens'][-2] + ' ' + event['request']['nlu']['tokens'][-1] in user_cards:
                    face_card = user_cards.pop(user_cards.index(
                        event['request']['nlu']['tokens'][-2] + ' ' + event['request']['nlu']['tokens'][-1]))
                    stage = 8
                    stage_2 = 8
                    text = 'Теперь верняя карта - ' + face_card
                    tts = text

    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': text,
            'tts': tts,
            'end_session': 'false'
        },
    }


def pull(deck):
    card_pull = deck.pop(randint(0, len(deck)))
    return [card_pull, deck]


def check_user(face, cards):
    a = []
    fa = face.split()
    if fa[-1] == 'цвета':
        a = cards
        return ['Ты можешь положить любую карту', a]
    for i in cards:
        if i.split()[0] == fa[0] or i.split()[-1] == fa[-1]:
            a.append(i)
    if len(a) > 1:
        return ['Ты можешь положить следующие карты: ', a]
    if a == 0:
        return ['Ты не можешь сходить, бери карты из колоды', 0]
    if len(a) == 1 and a != 0:
        return ['Ты можешь положить одну карту', a]
