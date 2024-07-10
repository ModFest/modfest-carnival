scoreboard players add #timerCounter wheelDuckTimer 1
execute if score #timerCounter wheelDuckTimer matches 120 run execute at @p run summon duck:duck ~ ~ ~
execute if score #timerCounter wheelDuckTimer matches 120 run scoreboard players set #timerCounter wheelDuckTimer 0