# x,y,z = char.Position; bow=Bladex.CreateEntity("arcarc","Arco",x,y,z,"Weapon"); ItemTypes.ItemDefaultFuncs(bow)
# quv=Bladex.CreateEntity("quiv","Carcaj",x,y,z); ItemTypes.ItemDefaultFuncs(quv); quv.Data.ArrowsLeft=10
import whrandom ## !!!

def CreateMuzzleFlash(parent):
	original = Bladex.GetEntity(parent.Name)
	x,y,z = original.Position
	flash = Bladex.CreateEntity(Bladex.GenerateEntityName(),"Entity Spot",x,y,z)
	flash.Color = 230, 95, 20
	flash.Visible = 0
	flash.Intensity = 13.0
	flash.Precission = 0.001
	Bladex.AddScheduledFunc(Bladex.GetTime()+0.016, FadeFlash,(flash.Name,), "Flashfade"+flash.Name)
	
def FadeFlash(spot):
	flash = Bladex.GetEntity(spot)
	if flash.Intensity > 9.0:
		flash.Intensity = 8.5
		Bladex.AddScheduledFunc(Bladex.GetTime()+0.016, FadeFlash,(flash.Name,), "Flashfade"+flash.Name)
	elif flash.Intensity == 8.5:
		flash.Intensity = 4.5
		Bladex.AddScheduledFunc(Bladex.GetTime()+0.016, FadeFlash,(flash.Name,), "Flashfade"+flash.Name)
	else:
		flash.SubscribeToList("Pin")
	
def CreateRandomArrows(qty, parent):
	original = Bladex.GetEntity(parent.Name)
	for q in range(qty):
		o = Bladex.CreateEntity(Bladex.GenerateEntityName(),original.Kind,original.Position[0], original.Position[1], original.Position[2])
		o.Arrow=1
		o.ExclusionMask = 1
		newX,newY,newZ,newP = original.Orientation[0]*whrandom.uniform(0.9,1.1),original.Orientation[1]*whrandom.uniform(0.9,1.1),original.Orientation[2]*whrandom.uniform(0.9,1.1),original.Orientation[3]*whrandom.uniform(0.9,1.1)
		o.Orientation = (newX,newY,newZ,newP)
		vx,vy,vz= o.Rel2AbsVector(0,0,-40000)
		o.Fly(vx,vy,vz)
		o.MessageEvent(MESSAGE_START_WEAPON,0,0)
		o.CastShadows=0
		o.Alpha = 0.0
		InitDataField.Initialise(o)
		Bladex.AddScheduledFunc(Bladex.GetTime()+2.0, ThrownWeaponStopFunc,(o.Name,),"Stop Weapon: "+o.Name)
		o.Data.PrevInflictHitFunc= o.InflictHitFunc
		o.InflictHitFunc= ThrownWeaponInflictHitFunc
		o.Data.ThrownBy= Bladex.GetEntity("Player1")

def EndDrawBowEventHandler(EntityName, EventName):
	me= Bladex.GetEntity(EntityName)
	#print EntityName+" EndDrawBowEventHandler, "+me.AnimName+": "+`me.AnmPos`
	if me.Data.AimPressed==0:
		me.Aim= 0
		arrow= Bladex.GetEntity(me.InvRight)
		if arrow:
			#print EntityName+" EndDrawBowEventHandler:Letting Arrow Fly"
			# exclude people from collision
			#arrow.ExclusionMask= arrow.ExclusionMask | B_SOLID_MASK_PERSON

			# play arrow sound
			me.Unlink(arrow)
			me.RemoveFromInventRight()
			UnGraspString (EntityName,"UnGraspString")
			# Release the arrow
			arrow.ExcludeHitFor(me)
			arrow.PutToWorld()

			# Let the arrow fly along its own Z axis
			CreateRandomArrows(7,arrow)
			newX,newY,newZ,newP = arrow.Orientation[0]*whrandom.uniform(0.9,1.1),arrow.Orientation[1]*whrandom.uniform(0.9,1.1),arrow.Orientation[2]*whrandom.uniform(0.9,1.1),arrow.Orientation[3]*whrandom.uniform(0.9,1.1)
			arrow.Orientation = (newX,newY,newZ,newP)
			arrow.CastShadows=0
			arrow.Alpha = 0.0
			if me.Data.NPC:
				vx,vy,vz= me.AimVector
			else:
				vx,vy,vz= arrow.Rel2AbsVector(0,0,-40000)
			arrow.Fly(vx,vy,vz)

			arrow.MessageEvent(MESSAGE_START_WEAPON,0,0)
			# arrow.MessageEvent(MESSAGE_START_TRAIL,0,0)

			# Arrange for the MESSAGE_STOP_WEAPON to be sent
			InitDataField.Initialise(arrow)
			Bladex.AddScheduledFunc(Bladex.GetTime()+2.0, ThrownWeaponStopFunc,(arrow.Name,),"Stop Weapon: "+arrow.Name)
			arrow.Data.PrevInflictHitFunc= arrow.InflictHitFunc
			arrow.InflictHitFunc= ThrownWeaponInflictHitFunc
			arrow.Data.ThrownBy= me

			soltar_sound=Bladex.CreateEntity(arrow.Name+"FlySound", "Entity Sound", 0, 0, 0)
			randsound = whrandom.randint(1,3)
			soltar_sound.SetSound("../../Sounds/sgfire_0"+`randsound`+".wav")
			CreateMuzzleFlash(arrow)
			# soltar_sound.SetSound("../../Sounds/ARCO-DISPARO-3.wav")
			soltar_sound.MinDistance=10000
			soltar_sound.MaxDistance=50000
			arrow.Link(soltar_sound)
			soltar_sound.PlaySound(0)
			#"ARCO-DISPARO-3.wav"
			#"M-CREAKCUERDA-44.wav"

			# Draw another arrow
			me.SetTmpAnmFlags(1,0,1,1,2,0)
			#print "Drawn another"
			me.LaunchAnmType ("b2")
			return
	#print EntityName+" EndDrawBowEventHandler:b3"
	me.LaunchAnmType ("b3")


def CheckRefireBowEventHandler(EntityName, EventName):
	me= Bladex.GetEntity(EntityName)
	#print EntityName+" CheckRefireBowEventHandler, "+me.AnimName+": "+`me.AnmPos`
	if me.InvRight:
		action= BInput.GetInputManager().GetInputActions().Find("Attack")
		if action and action.this!="NULL" and action.CurrentlyActivated():
			me.Aim= 1
			me.Data.AimPressed= 1

		if me.Data.AimPressed:
			arrow= Bladex.GetEntity(me.InvRight)
			if arrow:
				#print "CheckRefireBowEventHandler:Refire"
				GraspString (EntityName,"GraspString")
				me.DoActionWI ("b1", FixedFootAutoInterp, 0.3, 0.9)
				tensar_sound=Bladex.CreateEntity(arrow.Name+"RedrawSound", "Entity Sound", 0, 0, 0)
				tensar_sound.SetSound("../../Sounds/shotgun_use_01.wav")
				# tensar_sound.SetSound("../../Sounds/M-CREAKCUERDA-44.wav")
				tensar_sound.MinDistance=5000
				tensar_sound.MaxDistance=10000
				arrow.Link(tensar_sound)
				tensar_sound.PlaySound(0)
				return
		#else:
		#	print EntityName+" CheckRefireBowEventHandler, aimpressed: "+`me.Data.AimPressed`
		#	print EntityName+" CheckRefireBowEventHandler, InvRight: "+me.InvRight
		#print EntityName+" CheckRefireBowEventHandler:EndBowMode"
	EndBowMode(EntityName)
