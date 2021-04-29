from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.command()
const Discord=require('discord.js');
const intents=new Discord.Intents();
const client=new Discord.Client({ws:{intents:intents.ALL}});
var filepath="./config.json";
var config=require(filepath);

const fs=require("fs");

client.on('ready',() =>{
    console.log("login with "+client.user.tag+" now");
})

client.on(`message`, (msg) =>{
    const args = msg.content.split(" ");
    if(args[0]==='!addvc'){
        if(args.length<4){
            const embed=new Discord.MessageEmbed();
            embed.setTitle("Not enough arguments").setColor("RED").setDescription("Not enough arguments");
            msg.channel.send(embed);
            return;
        }
        fs.readFile("config.json",{encoding: "utf-8"},(err,file)=>{
            if(err){
                console.error(err);
            }
            else{
                var configdata=JSON.parse(file);
                configdata.create[configdata.create.length]=[args[1],args[2],args[3]];
                const configtext=JSON.stringify(configdata,undefined,4);
                fs.writeFile("config.json",configtext,{encoding: 'utf-8'},(err2)=>{
                    if(err){
                        console.error(err2);
                    }
                    else{
                        const embed=new Discord.MessageEmbed();
                        embed.setTitle("Set VC Channel").setColor("GREEN")
                            .setDescription("["+args[1]+","+args[2]+","+args[3]+"]\nhas been set")
                        msg.channel.send(embed);
                    }
                });
            }
        });
    }
    else if(args[0]==="!vclist"){
        fs.readFile("config.json",{encoding: "utf-8"},(err,file)=>{
            if(err){
                console.error(err);
            }
            else{
                var configdata=JSON.parse(file);
                const embed=new Discord.MessageEmbed();
                embed.setTitle("VC List").setColor("BLUE");
                var list="";
                list=list+"index | チャンネル名 | 新たなvc名\n"
                var index=0;
                for(const val of configdata.create){
                    index++;
                    const valchannel=msg.guild.channels.cache.get(val[0]);
                    if(valchannel==null||valchannel==undefined){
                        notchannel="not find";
                        list=list+String(index).padStart(5)+"　|　"+notchannel.padStart(15)+"　|　"+val[1].padStart(7)+"\n";
                    }
                    else{
                        list=list+String(index).padStart(5)+"　|　"+valchannel.name.padStart(15)+"　|　"+val[1].padStart(7)+"\n";
                    }
                }
                embed.setDescription(list);
                msg.channel.send(embed);
            }
        });
    }
    else if(args[0]==="!deletevc"){
        if(args.length<2){
            const embed=new Discord.MessageEmbed();
            embed.setTitle("Not enough arguments").setColor("RED").setDescription("Not enough arguments");
            msg.channel.send(embed);
            return;
        }
        fs.readFile("config.json",{encoding: "utf-8"},(err,file)=>{
            if(err){
                console.error(err);
            }
            else{
                var configdata=JSON.parse(file);
                configdata.create.splice(Number(args[1])-1,Number(args[1])-1);
                const configtext=JSON.stringify(configdata,undefined,4);
                fs.writeFile("config.json",configtext,{encoding: 'utf-8'},(err2)=>{
                    if(err){
                        console.error(err2);
                    }
                    else{
                        const embed=new Discord.MessageEmbed();
                        embed.setTitle("Delete VC Channel").setColor("YELLOW")
                            .setDescription("index:"+args[1]+"has been delete")
                        msg.channel.send(embed);
                    }
                });
            }
        });

    }
})

client.on('voiceStateUpdate', (oldState,newState) => onVoiceStateUpdate(oldState,newState));

async function onVoiceStateUpdate(oldState,newState){
    const newChannel = newState.channel;
    const oldChannel = oldState.channel;
    if(oldChannel!=null&&oldChannel!=undefined){
        fs.readFile("config.json",{encoding: "utf-8"},(err,file)=>{
            const configdata=JSON.parse(file);
            if(oldChannel!=null){
                for(const val of configdata["create"]){
                    const valchannel=oldChannel.guild.channels.cache.get(val[0]);
                    if(valchannel!=undefined&&valchannel!=null&&valchannel.parentID===oldChannel.parentID&&!(valchannel.id===oldChannel.id)&&valchannel!=undefined){
                        if(oldChannel.members.size==0){
                            oldChannel.delete();
                            return;
                        }
                    }
                }
            }
        });
    }
    if(newChannel!=null){
        fs.readFile("config.json",{encoding: "utf-8"},(err,file)=>{
            if(err){
                console.error(err.message);
                return;
            }
            const configdata=JSON.parse(file);
            var newchannelis=false;
            for(const val of configdata["create"]){
                if(val[0]===newChannel.id){
                    var newnamebase=val[1];
                    var vclimit=val[2];
                    newchannelis=true;
                    break;
                }
            }
            if(newchannelis===false){
                return;
            }
            const allchannels=newChannel.guild.channels.cache.filter(c=>c.type==="voice"&&c.parentID===newChannel.parentID&&!(c.id===newChannel.id));
            let numbers=[];
            allchannels.forEach(function(value,key){
                const number=value.name.replace(newnamebase+"-","");
                if(!(number==="")&&!(isNaN(number))){
                    numbers.push(Number(number));
                }
            });
            numbers.sort(
                function(a,b){
                    return(a<b?-1:1);
                });
            let newnumber;
            let handan=false;
            if(numbers.length===0){
                newnumber=1;
                handan=true;
            }
            else{
                newnumber=0;
                for(const val of numbers){
                    if(val===newnumber+1){
                        newnumber++;
                    }
                    else{
                        newnumber++;
                        handan=true;
                        break;
                    }
                }
            }
            if(handan===false){
                newnumber++;
            }
            let newname=newnamebase+"-"+String(newnumber);
            newChannel.guild.channels
                .create(newname,{type:"voice",parent:newChannel.parentID,userLimit:Number(vclimit)})
                .then((channel)=>{
                    const mem=newState.member;
                    mem.edit({channel:channel.id});
                })
                .catch(console.error);
        });
    }
}



client.login(config.token);
© 2021 GitHub, Inc.


bot.run(token)
