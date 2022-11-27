#!/usr/bin/env python3
# This code is licensed under the Gnu Public License
# version 3 or later.
# Code Copyright 2021 Peter Chubb
#
# Collects from the Australian Prayer Book
# Copyright 1978 The Church of England in Australia assocation.
#
from datetime import date, timedelta
from dateutil.parser import parse
from sys import argv

def calc_easter(year):
    "Returns Easter as a date object."
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1    
    return(date(year, month, day))


specials = {
    "12/24": "Christmas Eve",
    "12/25": "Christmas Day",
    "12/26": "Boxing Day; St Stephen",
    "12/27": "St John the Evangelist",
    "12/28": "The Innocents",
    "1/1": "New Year's Day/Circumcision",
    "1/6": "Epiphany",
    "2/2": "Presentation",
    "2/24": "St Matthias",
    "3/25": "Annunciation",
    "4/25": "St Mark; ANZAC day",
    "5/1": "St Philip and St James",
    "5/24": "Aldersgate Day (Wesley's Conversion)",
    "6/11": "St Barnabas",
    "6/24": "John the Baptist",
    "6/29": "St Peter",
    "7/22": "Mary Magdalen",
    "7/25": "St James",
    "8/8": "Transfiguration",
    "8/24": "St Bartholomew",
    "9/21": "St Matthew",
    "9/29": "St Michael and all Angels",
    "10/18": "St Luke",
    "10/28": "St Simon and St Jude",
    "10/31": "Reformation day",
    "11/1": "All Saints",
    "11/30": "St Andrew",
    "12/21": "St Thomas"
}

# Church year starts five weeks before Christmas.
# Christmas day is fixed on December 25
christmas_rel = [ 
    "Advent 4",
    "Advent 3", 
    "Advent 2",
    "Advent 1",
    "Christ the King", # Use Trinity 25
]

# All other dates are relative to Easter Sunday
# which is on a different date each year.
easter_rel = {
    -63: "Septuagesima",
    -56: "Sexagesima",
    -49: "Qunquagesima",
    -46: "Ash Wednesday",
    -42: "Lent 1",
    -35: "Lent 2",
    -28: "Lent 3",
    -21: "Lent 4",
    -14: "Lent 5",
    -7: "Palm Sunday",
    -2: "Good Friday",
    0: "Easter Day",
    7: "Easter 1",
    14: "Easter 2",
    21: "Easter 3",
    28: "Easter 4",
    35: "Easter 5",
    40: "Ascension Day",
    42: "Ascension 1",
    49: "Pentecost",
    56: "Trinity",
}

def church_date(d, incspecials = True):
    x = str(d.month) + '/' + str(d.day)
    if incspecials and x in specials:
        return specials[x]
    y = d.year
    easter_sun=calc_easter(y)
    days = (d - easter_sun).days
    if days < -63:
        # Epiphany relative
        epiphany = date(y, 1, 6)
        if d < epiphany:
            return "Christmas 2"
        return "Epiphany " + str(1 + ((d - epiphany).days // 7))
    if days > 56:
        # Christmas relative
        christmas = date(y, 12, 25)
        if christmas < d:
            return "Christmas 1"
        weeks_before_Christmas = (((christmas - d).days + 6) // 7)
        if weeks_before_Christmas < 6:
            return christmas_rel[weeks_before_Christmas - 1]
        week = (days - 56) // 7
        return "Trinity " + str(week)
    #print(days)
    if days in easter_rel:
        return easter_rel[days]
    return str(d)


collects = {
    "Advent 1":"""
Almighty God, give us grace that we may cast away the works of
darkness and put on the armour of light, now in the time of this
mortal life in which your Son Jesus Christ came among us in great
humility; that on the last day, when he comes again in his glorious
majesty to judge the living and the dead, we may rise to the life
immortal; through him who lives and reigns with you and the Holy
Spirit, now and for ever. Amen .
(AAPB p181)
""",
    "Advent 2":"""

Blessed Lord, you have caused all holy scriptures to be written for
our learning: grant us so to hear them, read, mark, learn, and in-
wardly digest them, that, encouraged and supported by your holy Word,
we may embrace and always hold fast the joyful hope of everlasting
life, which you have given us in our Saviour Jesus Christ. Amen.
(AAPB p182)
""",
    "Advent 3":"""
Lord Jesus Christ, at your first coming you sent your messenger to
prepare the way before you: grant that the ministers and stewards of
your mysteries may likewise make ready your way, by turning the hearts
of the disobedient to the ways of the righteous, that at your second
coming to judge the world we may be found an acceptable people in your
sight; for you live and reign with the Father and the Holy Spirit, now
and for ever. Amen.
(AAPB p242)

""",
    "Advent 4":"""

Raise up your great power, Lord, and come among us to save us; that,
although through our sins we are grievously hindered in running the
race that is set before us, your plentiful grace and mercy may
speedily help and deliver us; through the sufficiency of your Son our
Lord, to whom with you and the Holy Spirit be honour and glory, now
and for ever. Amen
(AAPB p245)
""",
    "Christmas 1":"""
Lord our God, you have given us as our example the life of Jesus
in his home: grant that all Christian families may be so bound
together in love and service that we may rejoice together, in your
heavenly home; through Jesus Christ our Lord, who lives and
reigns with you and the Holy Spirit, now and for ever. Amen .
(AAPB p189)
""",
    "Circumcision":"""
Almighty God, whose blessed Son was circumcised and for man’s
sake became obedient to the Law: purify our hearts and all our
members, so that we may die to all sinful desires and in all things
obey your holy will; through Jesus Christ our Lord.

""",
    "Christmas 2":"""
    (Use Circumcision)
Almighty God, whose blessed Son was circumcised and for man’s
sake became obedient to the Law: purify our hearts and all our
members, so that we may die to all sinful desires and in all things
obey your holy will; through Jesus Christ our Lord.
""",
    "Presentation":"""
Almighty and everliving God, we humbly pray that, as your only
Son was presented in the temple as a child in accordance with the
Law, so may we be dedicated to you with pure and clean hearts,
through him, our Saviour and Redeemer Jesus Christ our Lord.
(AAPB p270)
""",
    "Epiphany":"""
O God, who by the leading of a star manifested your beloved Son
to the gentiles: mercifully grant that we, who know you now by
faith, may after this life enjoy the splendour of your glorious God-
head; through Jesus Christ our Lord

""",
    "Epiphany 1":"""
Lord, mercifully receive the prayers of your people who call upon
you; and grant that we may perceive and know what things we
ought to do, and also may have grace and power faithfully to per-
form them; through Jesus Christ our Lord.
(AAPB p222)
""",
    "Epiphany 2": """
Almighty and everlasting God, ruler of all things in heaven and
earth, mercifully hear the supplications of your people, and grant
us your peace all the days of our life; through Jesus Christ our Lord.
(AAPB p223)
""",
    "Epiphany 3":"""
Almighty and everlasting God, mercifully look on our infirmities;
and in all our dangers and necessities stretch out your right hand
to help and defend us; through Jesus Christ our Lord.
(AAPB p260)
""",
    "Epiphany 4":"""
Lord God, you know us to be set in the midst of so many great
dangers that by reason of the frailty of our nature we cannot always
stand upright: grant us such strength and protection as may sup-
port us in all dangers and carry us through all temptations;
through Jesus Christ our Lord.
(AAPB p249)
""",
    "Epiphany 5":"""
Heavenly Father, keep your household the Church continually in
your true religion; that those who lean only on the hope of your
heavenly grace may always be defended by your mighty power;
through Jesus Christ our Lord.
(AAPB p238)
""",
    "Epiphany 6":""" 
Almighty Father, whose blessed Son was revealed so that he might
destroy the works of the devil and make us the children of God and
heirs of eternal life: grant that having this hope we may purify
ourselves as he is pure; that, when he shall appear again with power
and great glory, we may be made like him in his eternal and glorious
kingdom, where with you, Father, and with the Holy Spirit, he lives
and reigns, one God, for evermore.
(AAPB p190)
""",
    "Septuagesima":"""
Almighty God, creator of all things and giver of every good and
perfect gift, hear with favour the prayers of your people, that we
who are justly punished for our offences may mercifully be
delivered by your goodness, for the glory of your name; through
Jesus Christ our Saviour, who lives and reigns with you and the
Holy Spirit, one God, now and for ever.
(AAPB p257)
""",
    "Sexagesima":"""
Lord God, you know that we cannot put our trust in anything that
we do: help us to have faith in you alone, and mercifully defend
us by your power against all adversity; through Jesus Christ our
Lord.
(AAPB p246)
""",
    "Quinqagesima":"""
Lord, you have taught us that whatever we do without love is
worth nothing: send your Holy Spirit and pour into our hearts that
most excellent gift of love, the true bond of peace and of all virtues,
without which whoever lives is counted dead before you; grant this,
for your only Son Jesus Christ’s sake.
(AAPB 226)
""",
    "Lent 1":""" Lord Jesus Christ, for our sake you fasted forty days and forty
nights: give us grace to use such abstinence that, our flesh being
subdued to the spirit, we may always obey your will in righteousness
and true holiness, to your honour and glory; for you live and reign
with the Father and the Holy Spirit, one God, for evermore.  
(AAPB p193)
""",
    "Lent 2":"""
Almighty God, we confess that we have no power of ourselves to
help ourselves: keep us outwardly in our bodies and inwardly in
our souls, that we may be defended from all adversities that may
happen to the body, and from all evil thoughts that may assault
and hurt the soul; through Jesus Christ our Lord.
(AAPB p196)
""",
    "Lent 3":"""
We beseech you, almighty God, look on the heartfelt desires of your
servants, and stretch forth the right hand of your power to be our
defence against all our enemies; through Jesus Christ our Lord.
(AAPB p194)
""",
    "Lent 4":"""
Almighty God, grant that we, who justly deserve to be punished
for our sinful deeds, may in your mercy and kindness be pardoned
and restored; through our Lord and Saviour Jesus Christ.
(AAPB p197)
""",
    "Lent 5":"""
(Passion Sunday)
We beseech you, almighty God, to look in mercy on your people:
that by your great goodness they may be governed and preserved
evermore; through Jesus Christ our Lord.
(AAPB p199)
""",
    "Palm Sunday":"""
Almighty and everlasting God, in tender love towards mankind
you sent your Son, our Saviour Jesus Christ, to take our nature
upon him and to suffer death on the cross, that all mankind should
follow the example of his great humility: grant that we may follow
the example of his suffering, and also be made partakers of his
resurrection; through him who lives and reigns with you and the
Holy Spirit, now and for ever.
(AAPB p200)
""",
    "Easter Day":"""
Almighty God, you have conquered death through your dearly
beloved Son Jesus Christ and. opened to us the gate of everlasting
life: grant us by your grace to set our mind on things above, so that
by your continual help our whole life may be transformed; through
Jesus Christ our Lord, who is alive and reigns with you and the
Holy Spirit in everlasting glory.
(AAPB p209)
""",
    "Easter 1":"""
Almighty Father, you have given your only Son Jesus Christ to die
for our sins and to rise again for our justification: grant that we
may put away the old leaven of corruption and wickedness, and
always serve you in sincerity and truth; through the merits of Jesus
Christ our Lord.
(AAPB p210)
""",
    "Easter 2":"""
Almighty God, you have given your only Son to be for us both a
sacrifice for sin and also an example of godly life; give us grace that
we may always thankfully receive the immeasurable benefit of his
sacrifice, and also daily endeavour to follow in the blessed steps
of his most holy life; who now lives and reigns with you and the
Holy Spirit, one God, for evermore. Amen.
(AAPB p212)
""",
    "Easter 3":"""
Almighty God, you show to those who are in error the light of your
truth so that they may return into the way of righteousness: grant
to all who are admitted into the fellowship of Christ’s service that
they may renounce those things that are contrary to their
 profession and follow all such things as are agreeable to it; through 
our Lord Jesus Christ  
(AAPB p214)
""",
    "Easter 4":"""
Almighty God, you alone can order the unruly wills and passions
of sinful men: grant to your people that they may love what you
command and desire what you promise, that so, among the many
and varied changes of the world, our hearts may surely there be
fixed where true joys are to be found; through Jesus Christ our
Lord.  
(AAPB p213)
""",
    "Easter 5":"""
Heavenly Father, the giver of all good things, fill our hearts with
thankfulness, and grant that by your holy inspiration we may think
those things that are good, and by your merciful guidance may perform
them; through our Lord Jesus Christ.
(AAPB p215)
""",
    "Ascension Day":"""
Grant, we pray, almighty God, that as we believe your only begotten Son to have ascended into heaven, so we may also in heart and
mind there ascend, and with him continually dwell; who lives and
reigns with you and the Holy Spirit, one God, for ever and ever.  
(AAPB p217)
""",
    "Ascension 1":"""
O God, the king of glory, you have exalted your only Son Jesus
Christ with great triumph to your kingdom in heaven: leave us not
desolate, but send your Holy Spirit to strengthen us, and exalt us
to where our Saviour Christ has gone before, who lives and reigns
with you and the Holy Spirit, one God, for evermore. 
(AAPB p218)
""",
    "Pentecost":"""
Almighty God, who taught the hearts of your faithful people by
sending to them the light of your Holy Spirit: grant to us by the
same Spirit to have a right judgment in all things and always to
rejoice in his holy comfort; through the merits of Christ Jesus our
Saviour, who lives and reigns with you and the Holy Spirit, one
God, now and for ever  
(AAPB p219)
""",
    "Trinity":"""
Almighty and everlasting God, you have given us your servants
grace by the confession of a true faith to acknowledge the glory of
the eternal Trinity, and by your divine power to worship you as
One: we humbly pray that you would keep us steadfast in this faith
and evermore defend us from all adversities; through Christ our
Lord. 
(AAPB p220)
""",
    "Trinity 1":"""
Lord God, the strength of all who put their trust in you:
mercifully accept our prayers, and because through the weakness
of our mortal nature we can do nothing good without you, grant
us the help of your grace, that in keeping your commandments we
may please you both in word and deed; through Jesus Christ our
Lord. 
(AAPB p225)
""",
    "Trinity 2":"""
God. our refuge and strength, the author of all godliness, hear the
devout prayers of your Church: and grant that what we ask in faith
we may surely obtain; through Jesus Christ our Lord. AAPB 227
""",
    "Trinity 3":"""
Graciously hear us, Lord God; and grant that we, to whom you
have given the desire to pray, may by your mighty aid be defended
and strengthened in all dangers and adversities; through Jesus
Christ our Lord.  
(AAPB 258)
""",
    "Trinity 4":"""
Almighty God, the protector of all who put their trust in you, without
 whom nothing is strong, nothing is holy: increase and multiply
upon us your mercy, so that with you as our ruler and guide, we
may so pass through things temporal that we finally lose not the
things eternal; grant this, heavenly Father, for our Lord Jesus
Christ’s sake.
(AAPB p243)
""",
    "Trinity 5":"""
Almighty God, we pray that the course of this world may be so
peaceably ordered through your guidance that your church may
joyfully serve you in all godly quietness; through Jesus Christ our
Lord.  
(AAPB p183)
""",
    "Trinity 6":"""
    God our Father, you have prepared for those who love you such
good things as pass man’s understanding: pour into our hearts such
love towards you, that we, loving you above all things, may obtain
your promises which exceed all that we can desire; through Jesus
Christ our Lord.  
(AAPB p247)
""",
    "Trinity 7":"""
  Lord of all power and might, the author and giver of all good
things, graft in our hearts the love of your Name, increase in us
true religion, nourish us with all goodness, and so by your mercy
keep us; through Jesus Christ our Lord. Amen . 
(AAPB p240)
""",
    "Trinity 8":"""
Almighty God, whose never-failing providence governs all things
in heaven and earth: we humbly ask you to put away from us all
hurtful things, and to give us whatever may be profitable for us;
through Jesus Christ our Lord. Amen. 
(AAPB p233)
""",    
    "Trinity 9":"""
Grant us, Lord, we pray, the spirit to think and do always such
things as are right, that we who cannot do anything that is good
without you, may in your strength be able to live according to your
will; through Jesus Christ our Lord.
(AAPB p230)
""",
    "Trinity 10":"""
Let your merciful ears, Lord God, be open to the prayers of your
people; and so that they may obtain their petitions, make them
to ask such things as will please you; through Jesus Christ our Lord.
(AAPB p229)
""",
    "Trinity 11":"""
Lord God, you declare your almighty power chiefly in showing mercy and
pity: grant us such a measure of your grace that, running in the way
of your commandments, we may obtain your promises, and share in your
heavenly treasure; through Jesus Christ our Lord. Amen .
(AAPB p 256)
""",
    "Trinity 12":"""
Almighty and everlasting God, you are always more ready to hear
than we to pray, and constantly give more than either we desire
or deserve: pour down on us the abundance of your mercy, 
forgiving us those things of which our conscience is afraid, and giving
us those good things which we are not worthy to ask, except
through the merits and mediation of Jesus Christ, your Son our
Lord. Amen .
(AAPB p250)
""",
    "Trinity 13":"""
Merciful God, it is by your gift alone that your faithful people offer
you true and acceptable service; grant that we may so faithfully
serve you in this life that we fail not finally to obtain your heavenly
promises; through the merits of Jesus Christ our Lord.
(AAPB p262)
    """,
    "Trinity 14":"""
Almighty and eternal God, grant that we may grow in faith, hope,
and love; and that we may obtain what you promised, make us
love what you command; through Jesus Christ our Lord.
(AAPB p261)
""",
    "Trinity 15":"""
Keep your Church, Lord God, with your continual mercy, and 
because the frailty of man without you cannot but fall, keep us always
under your protection, and lead us to everything that makes for
our salvation; through Jesus Christ our Lord. Amen
(AAPB p232)
""",
    "Trinity 16":"""
Lord, let your continual pity cleanse and defend your church, and
because it cannot continue in safety without your aid, keep it 
evermore by your help and goodness; through Jesus Christ our Lord.
Amen .
(AAPB p255)
""",
    "Trinity 17":"""
    Lord, we pray that your grace may always uphold and encourage
us, and make us continually to be given to all good works; through
Jesus Christ our Lord. Amen
(AAPB p236)
""",
    "Trinity 18":"""
    Lord, give your people grace to withstand the temptations of the
world, the flesh, and the devil, and with pure hearts and minds
to follow you the only God; through Jesus Christ our Lord.
Amen. 
(AAPB p239)
""",
    "Trinity 19":"""
    Lord God, without you we are not able to please you; mercifully
grant that your Holy Spirit may in all things direct and rule our
hearts; through Jesus Christ our Lord. Amen
(AAPB p235)
""",
    "Trinity 20":"""
Almighty and merciful God, of your bountiful goodness keep us
from everything that may hurt us, that we may be ready in body
and soul cheerfully to accomplish whatever you want us to do;
through Jesus Christ our Lord.
(AAPB p263)
""",
    "Trinity 21":"""
Merciful Lord, grant to your faithful people pardon and peace,
that they may be cleansed from all their sins, and serve you with
a quiet mind; through Jesus Christ our Lord. Amen .
(AAPB p253)
""",
    "Trinity 22":"""
Father in heaven, keep your household the church steadfast in faith
and love, that through your protection it may be free from all
adversities, and may devoutly serve you in good works to the glory
of your name; through Jesus Christ our Lord.
(AAPB p265)
""",
    "Trinity 23":"""
God. our refuge and strength, the author of all godliness, hear the
devout prayers of your Church: and grant that what we ask in faith
we may surely obtain; through Jesus Christ our Lord.
(AAPB p227)
""",
    "Trinity 24":"""
    Lord, we pray, absolve your people from their offences; that
through your bountiful goodness we may be set free from the
chains of those sins which in our frailty we have committed: grant
this, heavenly Father, for the sake of Jesus Christ, our Lord and
Saviour. Amen
(AAPB p252)
""",
    "Trinity 25":""" 
Stir up, Lord, the wills of your faithful people, that they may
produce abundantly the fruit of good works, and receive your
abundant reward; through Jesus Christ our Lord.
(AAPB p266)  
""",
}

# Collects for non-Sundays
special_collects = {
    "Christ the King":"""
Stir up, Lord, the wills of your faithful people, that they may
produce abundantly the fruit of good works, and receive your
abundant reward; through Jesus Christ our Lord.
(AAPB p266)  
""",
    # Special Days
    "Boxing Day; St Stephen":"""
Lord Jesus Christ, grant that, in all our sufferings in witness to your
truth, we may learn to look steadfastly to heaven and see by faith
the glory that is to be revealed, and filled with the Holy Spirit may
learn to pray for our persecutors, as Stephen your first martyr
prayed for his murderers to you, blessed Jesus, where you stand
at the right hand of God to aid all who suffer for you, our only
mediator and advocate. Amen .
(AAPB p289)
""",
    "Christmas Day":"""
Almighty God, you have given us your only Son to take our nature
upon him and as at this time to be born of a pure virgin: grant
that we, being born again and made your children by adoption and
grace, may daily be renewed by your Holy Spirit; through our Lord
Jesus Christ, who lives and reigns with you and the Holy Spirit,
one God, for ever and ever. Amen .
(AAPB p188)
""",
    "Annunciation":"""
We beseech you, Lord, pour your grace into our hearts; that, as
we have known the incarnation of your Son Jesus Christ by the
message of an angel, so by his cross and passion we may be brought
to the glory of his resurrection, who lives and reigns with you and
the Holy Spirit, one God, for ever and ever.
(AAPB p272)
""",
    "St Matthias":"""
Almighty God, you chose your faithful servant Matthias to be
numbered among the twelve apostles in the place of Judas: grant
that your church may always be preserved from false apostles, and
may be guided by true and faithful pastors; through Jesus Christ
our Lord.
(AAPB p271)
""",
    "Ash Wednesday":"""
Almighty and everlasting God, you hate nothing that you have
made, and you forgive the sins of all who are penitent: create and
make in us new and contrite hearts, that we, lamenting our sins
and acknowledging our wretchedness, may obtain from you, the
God of all mercy, perfect remission and forgiveness; through Jesus
Christ our Lord.
(AAPB p192)
""",
    "Good Friday":"""
Almighty Father, look graciously upon this your family, for which
our Lord Jesus Christ was willing to be betrayed and given up into
the hands of wicked men, and to suffer death upon the cross; who
now lives and reigns with you and the Holy Spirit, one God, for
ever and ever.
(AAPB p204)
""",
    "Easter Eve":"""
Grant, Lord, that as we have been baptized into the death of your
dear Son our Saviour Jesus Christ, so by continually putting to
death our sinful desires we may die to sin and be buried with him,
and that through the grave and gate of death we may pass to our
joyful resurrection; for his sake who died and was buried and rose
again for us, your Son Jesus Christ our Lord.
(APPB p208)
""",
    "St Mark; ANZAC day":"""
Almighty God, we thank you for the gospel of your Son Jesus
Christ committed to us by the hand of your evangelist Saint Mark:
grant that we may not be carried away with every changing wind
of teaching, but may be firmly established in the truth of your
word; through Jesus Christ our Lord.
(AAPB p273)
""",
    "St John the Evangelist":"""
Merciful Lord, let your glory shine upon your Church; that,
enlightened by the teaching of your blessed apostle and evangelist
Saint John, we may walk in the light of your truth and come at
last to the splendour of eternal life; through Jesus Christ our Lord.
(AAPB p290)
""",
    "The Innocents":"""
Almighty God, whose loving purposes cannot be frustrated by the
wickedness of men, so that even infants may glorify you by their
deaths: strengthen us by your grace, that by the innocency of our
lives and the constancy of our faith even to death, we may glorify
your holy Name; through Jesus Christ our Lord.
(AAPB p291)
""",
    "St Philip and St James":"""
Almighty God, whom truly to know is eternal life: grant us per-
fectly to know your Son Jesus Christ to be the way, the truth, and
the life, that, following in the steps of your holy apostles Saint
Philip and Saint James, we may steadfastly walk in the way that
leads to eternal life; through Jesus Christ your Son our Lord.
    (AAPB p274)
    """,
    "St Barnabas":"""
Lord God Almighty, who endowed your apostle Barnabas with
faith and the Holy Spirit for the work to which he was called: do
not leave us destitute of your abundant gifts, or of grace to use them
always for your honour and glory; through Jesus Christ our Lord.
(AAPB p275)
""",
    "John the Baptist":"""
Almighty God, by whose providence your servant John the Baptist was
wonderfully born, and sent to prepare the way for your Son our Saviour
by preaching repentance: grant that we may truly repent according to
his teaching, and following his example may constantly speak the
truth, boldly rebuke vice, and patiently suffer for the truth’s sake;
through Jesus Christ our Lord.
(AAPB p276)
""",
    "St Peter": """
Almighty God, who by your Son Jesus Christ gave your apostle
Peter many excellent gifts, and commanded him earnestly to feed
your flock: enable, we pray, all bishops and pastors diligently to
preach your holy word, and your people obediently to follow it,
that they may receive the crown of everlasting glory; through Jesus
Christ our Lord.
(AAPB p277)
""",
    "Mary Magdelen":"""
Merciful God, whose Son Jesus Christ called Mary Magdalen to
be a witness to his resurrection: mercifully grant that by your grace
we may serve you in the power of his risen life; through Jesus Christ
our Lord.
(AAPB p278)
""",
    "St James the Apostle":"""
Merciful God, whose apostle James left his father, and all that he
had, and without delay obeyed the call of your Son Jesus Christ
and followed him: grant that no worldly affections may draw us
away from steadfast devotion to your service, but that we may be
always ready to do what you command; through Jesus Christ our
Lord.
(AAPB p279)
""",
    "Transfiguration":"""
Eternal God, our glorious King, whose Son Jesus Christ was seen
in splendour by his chosen witnesses: give us, your servants, faith
to see in him the true light and to walk in his way, that we may
be transformed into his likeness and live with him in glory; where
he lives and reigns with you and the Holy Spirit, one God, for ever
and ever.
(AAPB p280)
""",
    "St Bartholomew":"""
Almighty and eternal God, who gave your apostle Bartholomew
grace truly to believe and to preach your word: grant that your
Church may love that word, and both preach and receive it;
through Jesus Christ our Lord.
(AAPB p281)
""",
    "St Matthew":"""
Almighty God, whose beloved Son called Matthew from his place
of business to be an apostle and evangelist: set us free from all greed
and selfish love of money, to follow our Master Jesus Christ; who
lives and reigns with you and the Holy Spirit, now and for ever.
(AAPB p282)
""",
    "St Michael and all Angels":"""
Eternal God, by whom the ministries of angels and men have been
ordained and constituted in a wonderful order: grant that as your
holy angels always serve you in heaven, so by your appointment
they may help and defend us on earth; through our Lord and
Saviour Jesus Christ, who lives and reigns with you and the Holy
Spirit, one God, for evermore.
(AAPB p283)
""",
    "St Luke":"""
Almighty God, who called Luke the physician to be an evangelist
and physician of the soul: grant that through his teaching we may
know the certainty of the things which belong to your kingdom,
and that all the diseases of our souls may be healed; through the
merits of your Son Jesus Christ our Lord.
(AAPB p284)
""",
    "St Simon and St Jude":"""
Almighty God, you have built your Church on the foundation of
the apostles and prophets, with Jesus Christ himself as the chief
corner-stone: grant us to be so joined together in unity of spirit by
their doctrine, that we may grow into a holy temple, acceptable
to you; through Jesus Christ our Lord.
(AAPB p285)
""",
    "All Saints":"""
We praise you, heavenly Father, that you have knit together your
elect in one communion and fellowship in the mystical body of
your Son Christ our Lord; give us grace so to follow your blessed
saints in all virtuous and godly living, that we may come to those
inexpressible joys that you have prepared for those who love you;
through Jesus Christ our Lord.
(AAPB p286)
""",
    "St Andrew":"""
Almighty God, who gave such grace to your apostle Andrew that
he readily obeyed the call of your Son Jesus Christ and followed
him without delay: grant that we who are called by your holy word
may give ourselves at once to do what you command; through
Jesus Christ our Lord.
(AAPB p287)
""",
    "St Thomas":"""
Eternal God, who strengthened Thomas your apostle, when he was
in doubt, with sure and certain faith in the resurrection of your
Son our Lord Jesus Christ: grant that we may be not faithless but
believing, until we come to see our Saviour in his glory face to face;
who lives and reigns with you and the Holy Spirit, one God, now
and for ever.
(AAPB p288)
""",
   
}

def collect_for(dd):
    ret = []
    if dd.weekday() != 6:
        sun = dd - timedelta(days = dd.weekday())
    else:
        sun = dd
    day = church_date(dd)
    if day in special_collects:
        ret.append((day, special_collects[day], True))
    nonspecial = church_date(sun, incspecials = False)
    if nonspecial in collects:
        ret.append((nonspecial, collects[nonspecial], False))
    return ret

def print_collect(day):
    x = collect_for(day)
    for (dd, collect, special) in x:
        print(dd)
        if collect is None:
            print("Please add collect for " + dd + " to code")
            continue
        if special:
            print("Special day")
        print(collect)

if len(argv) == 1:
    # Print next Sunday's collect.
   today = date.today()
   day = today + timedelta(days = 6 - today.weekday())
   print_collect(day)
else:
    for d in argv[1:]:
        try:
            dx = parse(d)
            day = date(dx.year, dx.month, dx.day)
        except:
            print("Can't coerce %s to a date\n" % d)
            continue;
        print_collect(day)
