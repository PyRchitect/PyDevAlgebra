#############################################################################
# Generated by PAGE version 8.0
#  in conjunction with Tcl version 8.6
#  Mar 24, 2024 01:18:20 AM CET  platform: Windows NT
set vTcl(timestamp) ""
if {![info exists vTcl(borrow)]} {
    ::vTcl::MessageBox -title Error -message  "You must open project files from within PAGE."
    exit}


set vTcl(actual_gui_font_dft_desc)  TkDefaultFont
set vTcl(actual_gui_font_dft_name)  TkDefaultFont
set vTcl(actual_gui_font_text_desc)  TkTextFont
set vTcl(actual_gui_font_text_name)  TkTextFont
set vTcl(actual_gui_font_fixed_desc)  TkFixedFont
set vTcl(actual_gui_font_fixed_name)  TkFixedFont
set vTcl(actual_gui_font_menu_desc)  TkMenuFont
set vTcl(actual_gui_font_menu_name)  TkMenuFont
set vTcl(actual_gui_font_tooltip_desc)  TkDefaultFont
set vTcl(actual_gui_font_tooltip_name)  TkDefaultFont
set vTcl(actual_gui_font_treeview_desc)  TkDefaultFont
set vTcl(actual_gui_font_treeview_name)  TkDefaultFont
########################################### 
set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) gray40
set vTcl(analog_color_p) #c3c3c3
set vTcl(analog_color_m) beige
set vTcl(tabfg1) black
set vTcl(tabfg2) white
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(actual_gui_menu_active_fg)  #000000
########################################### 
set vTcl(pr,autoalias) 1
set vTcl(pr,relative_placement) 1
set vTcl(mode) Absolute
set vTcl(project_theme) xpnative



proc vTclWindow.top1 {base} {
    global vTcl
    if {$base == ""} {
        set base .top1
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    set target $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background SystemButtonFace -highlightbackground SystemButtonFace \
        -highlightcolor SystemWindowText 
    wm focusmodel $top passive
    wm geometry $top 510x700+785+102
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 3844 1061
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    set toptitle "Toplevel 0"
    wm title $top $toptitle
    namespace eval ::widgets::${top}::ClassOption {}
    set ::widgets::${top}::ClassOption(-toptitle) $toptitle
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    set vTcl(real_top) {}
    ttk::button "$top.tBu47" \
        -text "Izbrisi" -compound left -style "btn_unos.TButton" \
        -style btn_unos.TButton 
    vTcl:DefineAlias "$top.tBu47" "btn_izbrisi" vTcl:WidgetProc "Toplevel1" 1
    ttk::button "$top.tBu49" \
        -text "Spremi" -compound left -style "btn_unos.TButton" \
        -style btn_unos.TButton 
    vTcl:DefineAlias "$top.tBu49" "btn_spremi" vTcl:WidgetProc "Toplevel1" 1
    ::vTcl::widgets::ttk::labelframe::createCmd "$top.tLa47" \
        -text "Temperatura [C]" -width 480 -height 95 \
        -style "frm.TLabelframe" -style frm.TLabelframe 
    vTcl:DefineAlias "$top.tLa47" "frm_gumbi" vTcl:WidgetProc "Toplevel1" 1
    ::vTcl::widgets::ttk::labelframe::createCmd "$top.tLa49" \
        -text "Tlak [kPa]" -width 480 -height 270 -style "frm.TLabelframe" \
        -style frm.TLabelframe 
    vTcl:DefineAlias "$top.tLa49" "frm_DB" vTcl:WidgetProc "Toplevel1" 1
    set site_3_0 $top.tLa49
    vTcl::widgets::ttk::scrolledlistbox::CreateCmd "$site_3_0.scr71" \
        -background SystemButtonFace -height 75 \
        -highlightbackground SystemButtonFace \
        -highlightcolor SystemWindowText -width 125 
    vTcl:DefineAlias "$site_3_0.scr71" "box_tlak" vTcl:WidgetProc "Toplevel1" 1

    $site_3_0.scr71.01 configure -background SystemButtonFace \
        -cursor xterm \
        -disabledforeground #b4b4b4 \
        -font "-family {Segoe UI} -size 10" \
        -foreground SystemWindowText \
        -height 3 \
        -highlightcolor #d9d9d9 \
        -relief solid \
        -selectbackground #d9d9d9 \
        -selectforeground black \
        -width 10
    ttk::label "$site_3_0.tLa73" \
        -font "-family {Segoe UI} -size 9" -relief flat -anchor w \
        -justify left -text "Unutar kuće:" -compound left \
        -style "lbl_unos.TLabel" -style lbl_unos.TLabel 
    vTcl:DefineAlias "$site_3_0.tLa73" "lbl_tlak_kuca_unutra" vTcl:WidgetProc "Toplevel1" 1
    ttk::label "$site_3_0.tLa72" \
        -font "-family {Segoe UI} -size 18" -relief flat -anchor w \
        -justify left -text "0000" -compound left -style "lbl_unos.TLabel" \
        -style lbl_unos.TLabel 
    vTcl:DefineAlias "$site_3_0.tLa72" "lbl_tlak_kuca_unutra_v" vTcl:WidgetProc "Toplevel1" 1
    ttk::label "$site_3_0.tLa74" \
        -font "-family {Segoe UI} -size 9" -relief flat -anchor w \
        -justify left -text "Izvan kuće" -compound left \
        -style "lbl_unos.TLabel" -style lbl_unos.TLabel 
    vTcl:DefineAlias "$site_3_0.tLa74" "lbl_tlak_kuca_vani" vTcl:WidgetProc "Toplevel1" 1
    ttk::label "$site_3_0.tLa75" \
        -font "-family {Segoe UI} -size 18" -relief flat -anchor w \
        -justify left -text "0000" -compound left -style "lbl_unos.TLabel" \
        -style lbl_unos.TLabel 
    vTcl:DefineAlias "$site_3_0.tLa75" "lbl_tlak_izvan_kuce_v" vTcl:WidgetProc "Toplevel1" 1
    place $site_3_0.scr71 \
        -in $site_3_0 -x 0 -relx 0.042 -y 25 -width 0 -relwidth 0.375 \
        -height 155 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tLa73 \
        -in $site_3_0 -x 250 -y 20 -width 100 -relwidth 0 -height 22 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tLa72 \
        -in $site_3_0 -x 250 -y 40 -width 100 -relwidth 0 -height 40 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tLa74 \
        -in $site_3_0 -x 250 -y 100 -width 100 -relwidth 0 -height 22 \
        -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.tLa75 \
        -in $site_3_0 -x 250 -y 120 -width 100 -relwidth 0 -height 40 \
        -relheight 0 -anchor nw -bordermode ignore 
    ::vTcl::widgets::ttk::labelframe::createCmd "$top.tLa48" \
        -text "Vlažnost [%]" -width 480 -height 360 -style "frm.TLabelframe" \
        -style frm.TLabelframe 
    vTcl:DefineAlias "$top.tLa48" "frm_PIN" vTcl:WidgetProc "Toplevel1" 1
    set site_3_0 $top.tLa48
    vTcl::widgets::ttk::scrolledlistbox::CreateCmd "$site_3_0.scr51" \
        -background SystemButtonFace -height 75 \
        -highlightcolor SystemWindowText -width 125 
    vTcl:DefineAlias "$site_3_0.scr51" "box_vlaznost" vTcl:WidgetProc "Toplevel1" 1

    $site_3_0.scr51.01 configure -background SystemButtonFace \
        -cursor xterm \
        -disabledforeground #b4b4b4 \
        -font "-family {Segoe UI} -size 10" \
        -foreground SystemWindowText \
        -height 3 \
        -highlightcolor #d9d9d9 \
        -relief solid \
        -selectbackground #d9d9d9 \
        -selectforeground black \
        -width 10
    place $site_3_0.scr51 \
        -in $site_3_0 -x 20 -y 25 -width 180 -height 155 -relheight 0 \
        -anchor nw -bordermode ignore 
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.tBu47 \
        -in $top -x 420 -y 650 -width 70 -height 30 -anchor nw \
        -bordermode ignore 
    place $top.tBu49 \
        -in $top -x 330 -y 650 -width 70 -height 30 -anchor nw \
        -bordermode ignore 
    place $top.tLa47 \
        -in $top -x 15 -y 10 -width 480 -relwidth 0 -height 200 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.tLa49 \
        -in $top -x 15 -y 430 -width 400 -relwidth 0 -height 200 -relheight 0 \
        -anchor nw -bordermode ignore 
    place $top.tLa48 \
        -in $top -x 15 -y 220 -width 480 -relwidth 0 -height 200 -relheight 0 \
        -anchor nw -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

proc 36 {args} {return 1}


Window show .
set btop1 ""
if {$vTcl(borrow)} {
    set btop1 .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop1 $vTcl(tops)] != -1} {
        set btop1 .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop1
Window show .top1 $btop1
if {$vTcl(borrow)} {
    $btop1 configure -background plum
}

