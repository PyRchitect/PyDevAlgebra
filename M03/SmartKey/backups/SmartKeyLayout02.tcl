#############################################################################
# Generated by PAGE version 8.0
#  in conjunction with Tcl version 8.6
#  Feb 23, 2024 12:34:03 PM CET  platform: Windows NT
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
set vTcl(mode) Relative
set vTcl(project_theme) default



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
        -background #d9d9d9 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 
    wm focusmodel $top passive
    wm geometry $top 510x671+786+201
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
    ::vTcl::widgets::ttk::labelframe::createCmd "$top.tLa49" \
        -text "Tlabelframe" -width 480 -height 186 
    vTcl:DefineAlias "$top.tLa49" "TLabelframe1_1_1" vTcl:WidgetProc "Toplevel1" 1
    ::vTcl::widgets::ttk::labelframe::createCmd "$top.tLa47" \
        -text "Tlabelframe" -width 480 -height 95 
    vTcl:DefineAlias "$top.tLa47" "TLabelframe1" vTcl:WidgetProc "Toplevel1" 1
    set site_3_0 $top.tLa47
    button "$site_3_0.but50" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "Z" 
    vTcl:DefineAlias "$site_3_0.but50" "Button1" vTcl:WidgetProc "Toplevel1" 1
    button "$site_3_0.but51" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "O" 
    vTcl:DefineAlias "$site_3_0.but51" "Button2" vTcl:WidgetProc "Toplevel1" 1
    place $site_3_0.but50 \
        -in $site_3_0 -x 0 -relx 0.042 -y 0 -rely 0.286 -width 50 -relwidth 0 \
        -height 50 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but51 \
        -in $site_3_0 -x 0 -relx 0.854 -y 0 -rely 0.286 -width 50 -relwidth 0 \
        -height 50 -relheight 0 -anchor nw -bordermode ignore 
    ::vTcl::widgets::ttk::labelframe::createCmd "$top.tLa48" \
        -text "Tlabelframe" -width 480 -height 316 
    vTcl:DefineAlias "$top.tLa48" "TLabelframe1_1" vTcl:WidgetProc "Toplevel1" 1
    set site_3_0 $top.tLa48
    button "$site_3_0.but53" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "2" 
    vTcl:DefineAlias "$site_3_0.but53" "Button4" vTcl:WidgetProc "Toplevel1" 1
    button "$site_3_0.but52" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "1" 
    vTcl:DefineAlias "$site_3_0.but52" "Button3" vTcl:WidgetProc "Toplevel1" 1
    button "$site_3_0.but54" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "3" 
    vTcl:DefineAlias "$site_3_0.but54" "Button4_1" vTcl:WidgetProc "Toplevel1" 1
    button "$site_3_0.but55" \
        -activebackground #d9d9d9 -activeforeground black -background #d9d9d9 \
        -disabledforeground #a3a3a3 -font "-family {Segoe UI} -size 9" \
        -foreground #000000 -highlightbackground #d9d9d9 \
        -highlightcolor #000000 -text "4" 
    vTcl:DefineAlias "$site_3_0.but55" "Button4_1_1" vTcl:WidgetProc "Toplevel1" 1
    place $site_3_0.but53 \
        -in $site_3_0 -x 0 -relx 0.167 -y 0 -rely 0.301 -width 50 -relwidth 0 \
        -height 50 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but52 \
        -in $site_3_0 -x 0 -relx 0.042 -y 0 -rely 0.301 -width 50 -relwidth 0 \
        -height 50 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but54 \
        -in $site_3_0 -x 0 -relx 0.292 -y 0 -rely 0.301 -width 50 -relwidth 0 \
        -height 50 -relheight 0 -anchor nw -bordermode ignore 
    place $site_3_0.but55 \
        -in $site_3_0 -x 0 -relx 0.042 -y 0 -rely 0.475 -width 50 -relwidth 0 \
        -height 50 -relheight 0 -anchor nw -bordermode ignore 
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.tLa49 \
        -in $top -x 0 -relx 0.029 -y 0 -rely 0.7 -width 0 -relwidth 0.941 \
        -height 0 -relheight 0.277 -anchor nw -bordermode ignore 
    place $top.tLa47 \
        -in $top -x 0 -relx 0.029 -y 0 -rely 0.015 -width 0 -relwidth 0.941 \
        -height 0 -relheight 0.142 -anchor nw -bordermode ignore 
    place $top.tLa48 \
        -in $top -x 0 -relx 0.029 -y 0 -rely 0.194 -width 0 -relwidth 0.941 \
        -height 0 -relheight 0.471 -anchor nw -bordermode ignore 

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

