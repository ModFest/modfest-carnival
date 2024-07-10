# function mirthdew_encore:activate
execute as @n[tag=mirthdew_encore_activation_marker] at @s run fill ~ ~ ~ ~ ~ ~ minecraft:redstone_block replace minecraft:gold_block
tellraw @s {"text":"A Passage Is Opened...","italic":true,"color":"gray"}
playsound minecraft:block.iron_door.open master @s ~ ~ ~ 1 0 1
playsound minecraft:block.sculk_shrieker.shriek