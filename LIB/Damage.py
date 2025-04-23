	# Check type of weapon
	if thrown_flag and weapon.Arrow:
		weapon.MessageEvent(Reference.MESSAGE_STOP_WEAPON,0,0)
		weapon.MessageEvent(Reference.MESSAGE_STOP_TRAIL,0,0)
		weapon.Stop(x, y, z)
		# Check type of damage
		if me and (not me.Data.Mutilate) and DamageNode!=-1 and DamageZone!=Reference.BODY_HEAD and me.Life>0.0:
			# print "DamageNode is" +`DamageNode`+ ". DamageZone is" +`DamageZone`
			me.LinkToNode(weapon, DamageNode)
			sticktime= (3.0)/weapon.Mass
			# print "object "+weapon.Name+" of kind "+weapon.Kind+" of mass "+`weapon.Mass`+" sticking for "+`sticktime`+" seconds"
			Bladex.AddScheduledFunc (Bladex.GetTime()+sticktime, StuckWeaponFall, (weapon.Name, VictimName), weapon.Name+"_StuckWeaponFall")
			if weapon.StickFunc:
				weapon.StickFunc (weapon.Name, me.Name)
		else:
			weapon.Impulse (0.0,1.0,0.0)
		if me.Life <= 0.0 and DamageZone==Reference.BODY_HEAD:
			deCap = me.SeverLimb(1)
			if deCap: deCap.Impulse(0,-10000,0)
