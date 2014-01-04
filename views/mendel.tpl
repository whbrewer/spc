%include header title='confirm'

<html lang=en>
<head>
<title>Mendel - web interface</title>
<link type="text/css" rel="StyleSheet" href="/static/tab.webfx.css"/>
<link type="text/css" rel="StyleSheet" href="/static/start.css" />
<script type="text/javascript" src="/static/tabpane.js"></script>
<script type="text/javascript" src="/static/general.js"></script>
<script type="text/javascript" src="/static/mendel/mendel.js"></script>
</head>

%include navbar

<body onload="fxn_init()" bgcolor=ffffff>
<table width=550><tr><td valign=top><em>Note: using default parameters<br> </em><br></td><font color=red></font>
<!-- 
<td align=right valign=bottom>
<form name="template_form" method=post action="start.pl">
<select name="template" onChange="template_form.submit()">
<option SELECTED VALUE="">Choose parameter template...  <option VALUE=".human">Human and similar<option VALUE=".mito">Human Mitochondria<option VALUE=".yeast">Yeast and similar<option VALUE=".hiv">HIV and similar<option VALUE=".flu">Influenza and similar
</select>
-->
<input type="hidden" name="browser" value="Netscape">
<input type="hidden" name="version" value="2.2.5">
<input type="hidden" name="quota" value="16384">
<input type="hidden" name="user_id" value="wes">
</form>
</td>
</tr>
</table>

<form name="mendel_input" method=post action="/{{app}}/confirm" onsubmit="fxn_set_caseid()"><input type="hidden" name="user_id" value="wes">

<br>
<INPUT class="start" type="submit" value="Submit" accesskey="X">

<!-- <div class="navbar"> -->
             <input class="" type="text" name="case_id" value=""  
                         placeholder="caseid"
                   title="Case ID must be 6 characters" accesskey="C">
            <input class="label" type="text" name="description"
                   placeholder="short description about this run"
                   title="Label or description (optional)">
            <input class="css-checkbox" type="checkbox" name="caseid_cb" 
                   title="Generate a new random Case ID (U)"
                   onclick="fxn_set_this_caseid()" accesskey="U" tabindex="101">
            <div class="tribe" id="tribediv" style="display:none">
                Tribe:
            <select name="tribe_id">
                   <option VALUE=".001">.001</option>
                   <option VALUE=".002">.002</option>
            </select>
            </div> 
<!-- </div> -->

<div class="tab-pane" id="tab-pane-1">

<div class="tab-page">
<h2 class="tab">basic</h2>

<table>
<table>
   <tr><td><LABEL for="mutn_rate">
       1. <a class="plain" href="/static/mendel/help.html#nmpo" 
                 id="mutn_rate" target="status" 
                 title="mutn_rate" tabindex="102">
              Total non-neutral mutation rate:<br>
              &nbsp;&nbsp;&nbsp;
              (per individual per generation)</a> </LABEL></td>
    <td><INPUT type="text" name="mutn_rate" accesskey="1" 
                   value="{{mutn_rate}}"
                   onchange="compute_u()"
                   title="0 - 10,000; can be  fraction e.g. 0.5"></td>
        <td></td>
     </tr>
     <tr>
    <td><LABEL for="frac_fav_mutn">
       2. <a class="plain" href="/static/mendel/help.html#fomb" 
                 target="status" title="frac_fav_mutn" tabindex="103">
              Beneficial/deleterious ratio within non-neutral mutations:</a> 
            </LABEL></td>
    <td><INPUT type="text" name="frac_fav_mutn" accesskey="3" 
                   value="{{frac_fav_mutn}}" 
                   onchange="compute_u();check_value(this.value,0,1)"
                   title="0.0 - 1.0 (e.g. if 1:1000, enter 0.001)"></td>
        <td></td>
     </tr>
     <tr>
    <td><LABEL for="uben">
       &nbsp;&nbsp;&nbsp; <a class="plain" href="/static/mendel/help.html#fomb" target="status">
              <font color="grey">beneficial mutation rate:</font></</a> </LABEL></td>
    <td><INPUT name="uben" type="text" readOnly=true></td>
        <td></td>
     </tr>
     <tr>
    <td><LABEL for="udel">
       &nbsp;&nbsp;&nbsp; <a class="plain" href="/static/mendel/help.html#fomb" target="status">
              <font color="grey">deleterious mutation rate:</font></</a> </LABEL></td>
    <td><INPUT name="udel" type="text" readOnly=true></td>
        <td></td>
     </tr>
     <tr>
    <td><LABEL for="reproductive_rate">
       3. <a class="plain" href="/static/mendel/help.html#opf" target="status"
               id="opf" title="reproductive_rate" tabindex="104">
               Reproduction rate:</a> </LABEL></td>
    <td><INPUT type="text" name="reproductive_rate" accesskey="4" 
                   onchange="fxn_opf(this.value,1,6)"
                   value="{{reproductive_rate}}" title="1 - 6"></td>
        <td></td>
     </tr>
     <tr>
    <td><LABEL for="pop_size">
       4. <a class="plain" href="/static/mendel/help.html#popsize" target="status"
               id="pop" title="pop_size" tabindex="105">
              Population size (per subpopulation):</a> </LABEL></td>
    <td><INPUT type="text" name="pop_size" value="{{pop_size}}" 
                   accesskey="5" onchange="check_value(this.value,2,50000)"
                   title="2 - 50,000"></td>
        <td></td>
     </tr>
     <tr>
    <td><LABEL for="num_generations">
       5. <a class="plain" href="/static/mendel/help.html#ngen" target="status"
              id="gen" title="num_generations" tabindex="106">
              Generations:</a> </LABEL></td>
    <td><INPUT type="text" name="num_generations" accesskey="6" 
                   onchange="check_value(this.value,1,100000)"
                   value="{{num_generations}}" 
                   title="1 - 100,000"></td>
        <td></td>
     </tr>

<!--
     <tr><td><a class="plain" href="/static/mendel/help.html#adv" target="status"
                <u>A</u>dvanced settings?</a> </td>
         <td>
              <table><tr><td width=80>
              <input type="checkbox" name="advsel" id="advsel" 
                onclick="show_hide_advanced()" accesskey="A"
                title="Show/hide advanced parameters"></td>
              <td></td>
              </tr></table>
-->

</td></tr>
</table>
</td><td valign=top>
<!--
<font size="+1">Computed Parameters</font> 
<table>
<tr><td><font color="grey">Neutral mutation rate:<font></td><td></td></tr>
<tr><td><font color="grey">Beneficial mutation rate:</font></td><td></td></tr>
<tr><td><font color="grey">Deleterious mutation rate:</font></td><td></td></tr>
</table>
-->
</td></tr></table>
</div>

<!--*************************** ADVANCED PANE *******************************-->
<div class="tab-page">
<h2 class="tab">mutation</h2>

    <table>
       <tr>
          <td width=350>1. Distribution type:</td>
          <td>
        <select name="fitness_distrib_type" 
                        onchange="fxn_fitness_distrib_type_change()">
        <option SELECTED VALUE="1">Natural distribution (Weibull)<option VALUE="0">All mutations equal<option VALUE="2" readOnly=true>All mutations neutral<option VALUE="3" readOnly=true>Weibull + second mode
        </select>
          </td>
       </tr>
    </table>

     <div id="ufe_div" style="display:none">
     <table>
     <tr>
        <td width=350><LABEL for="uniform_fitness_effect_del">
           <a class="plain" href="/static/mendel/help.html#fdt" 
            title="uniform_fitness_effect_del" target="status">
         &nbsp;&nbsp;&nbsp;
         a. equal effect for each deleterious mutation:</a></LABEL></td>
        <td><input type="text" name="uniform_fitness_effect_del"
           value="{{uniform_fitness_effect_del}}"></td>
     </tr>     
     <tr>
        <td width=350><LABEL for="uniform_fitness_effect_fav">
           <a class="plain" href="/static/mendel/help.html#fdt" 
            title="{{uniform_fitness_effect_fav}}" target="status">
         &nbsp;&nbsp;&nbsp;
         b. equal effect for each beneficial mutation:</a></LABEL></td>
        <td><input type="text" name="uniform_fitness_effect_fav"
               value="0.0001"></td>
     </tr>     
     </table>      
     </div>
     
<div id="weibull_div" style="display:none">
    <a class="plain" href="/static/mendel/help.html#psddme" target="status"
                tabindex="107">
     &nbsp;&nbsp;&nbsp;
      Parameters shaping Weibull distribution of mutation effects:</a>
     <table>        
     
     <tr>
        <td width=350><LABEL for="genome_size">
         &nbsp;&nbsp;&nbsp;
               a. <a class="plain" href="/static/mendel/help.html#hgs" 
                         target="status" title="genome_size" tabindex="108">
                   functional genome size:</a><br> 
         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
             <font size="-2">&rarr; G<sub>functional</sub> = G<sub>actual</sub> - G<sub>junk</sub></font> </LABEL> </td>
        <td><INPUT type="text" name="genome_size" id="hgs" accesskey="1"
                   value="{{genome_size}}"
                   onchange="check_value(this.value,100,1e11)"
                   title="100 - 100 billion"></td>
     </tr>     
     
     <tr>
        <td><LABEL for="high_impact_mutn_fraction">
            &nbsp;&nbsp;&nbsp;
           b. <a class="plain" href="/static/mendel/help.html#himf"
                 target="status" title="high_impact_mutn_fraction"
                         tabindex="109">
        fraction of del. mutations with "major effect": </a></LABEL></td>
        <td><input type="text" name="high_impact_mutn_fraction"
                   value="{{high_impact_mutn_fraction}}"
                   onchange="check_value(this.value,0.0001,0.9)"
                   title="0.0001 - 0.9"></td>
     </tr>     
     
     <tr>
        <td><LABEL for="high_impact_mutn_threshold">
           &nbsp;&nbsp;&nbsp;
        c. <a class="plain" href="/static/mendel/help.html#himt" 
               target="status" title="high_impact_mutn_threshold" 
               tabindex="110">
               minimum del. effect defined as "major":</a></LABEL></td>
        <td><input type="text" name="high_impact_mutn_threshold"
           value="{{high_impact_mutn_threshold}}" 
                   onchange="check_value(this.value,0.01,0.9)"
                   title="0.01 - 0.9"></td>
     </tr>     
     <tr><td>      
       &nbsp;&nbsp;&nbsp;
        <a class="plain" href="/static/mendel/help.html#rdbm" target="status"
        tabindex="111" title="max_fav_fitness_gain">
            d. maximum beneficial fitness effect:</a></td>
        <td><input type="text" name="max_fav_fitness_gain" accesskey="2"
           value="{{max_fav_fitness_gain}}" title="0.000001 - 0.01"></td>
     </tr>
     
<!--
     <tr>
        <td width=350><LABEL for="max_fav_fitness_gain">
            &nbsp;&nbsp;&nbsp;
     &bull;     <a class="plain" href="/static/mendel/help.html#mffg" tabindex="112"
        target="status" title="max_fav_fitness_gain">maximal
           beneficial effect per mutation:</a></LABEL></td>
     </tr>     
-->
    <input type="hidden" name="max_fav_fitness_gain" value="{{max_fav_fitness_gain}}">
     
<!--
     <tr>
        <td><LABEL for="num_initial_fav_mutn">
            &nbsp;&nbsp;&nbsp;
          &bull; <a class="plain" href="/static/mendel/help.html#nifm"
                     tabindex="113"
                      target="status" title="num_initial_fav_mutn">
                      number of initial beneficial loci:</a></LABEL></td>
        <td><input type="text" name="num_initial_fav_mutn"
                   value="0" 
                   title="0 - 10,000"></td>
     </tr>     
-->
    <input type="hidden" name="num_initial_fav_mutn" value="{{num_initial_fav_mutn}}">
     
   </table>
</div>

<hr>

     <!-- Note: the value specified for a checkbox is sent
                     only if box is checked -->
             
     <table><tr><td width=350>
        <a class="plain" href="/static/mendel/help.html#cr" target="status"
           tabindex="115">2. Mutations &mdash; dominant vs. recessive?</a> </td>
          <td></td>
     </tr></table>
     
     
     <div id="crdiv">
     <table>
     <tr>
        <td width=350><LABEL for="fraction_recessive">
            &nbsp;&nbsp;&nbsp;
        a. <a class="plain" href="/static/mendel/help.html#fr"
              target="status" title="fraction_recessive"
                      tabindex="116">fraction recessive (rest dominant):</a></LABEL></td>
        <td><input type="text" name="fraction_recessive"
                   value="{{fraction_recessive}}"
                   onchange="check_value(this.value,0,1)"
                   id="fraction_recessive"
                   title="0.0 - 1.0" accesskey="3"></td>
     </tr>     
     <tr>
        <td><LABEL for="recessive_hetero_expression">
         &nbsp;&nbsp;&nbsp;
             b. <a class="plain" href="/static/mendel/help.html#rhe" 
                   tabindex="117" target="status" 
                   title="recessive_hetero_expression">
               expression of recessive mutations (in heterozygote):</a>
            </LABEL></td>
        <td><input type="text" name="recessive_hetero_expression"
                value="{{recessive_hetero_expression}}"
                onchange="check_value(this.value,0,0.5)"
                title="0.0 - 0.5"></td>
     </tr>  
     <tr>
        <td><LABEL for="dominant_hetero_expression">
         &nbsp;&nbsp;&nbsp;
         c. <a class="plain" href="/static/mendel/help.html#dhe"
               tabindex="118"
               target="status" title="dominant_hetero_expression">
                   expression of dominant mutations (in heterozygote):</a>
            </LABEL></td>
        <td><input type="text" name="dominant_hetero_expression"
                value="{{dominant_hetero_expression}}"
                onchange="check_value(this.value,0.5,1.0)"
                title="0.5 - 1.0"></td>
     </tr>  
     </table>   
     </div>
     
<hr>
     <table><tr>
     <td width=350>
        <a class="plain" href="/static/mendel/help.html#cmenam" target="status"
          tabindex="118">
          3. Combine mutations effects non-additively?</a> </td>
     <td> <input type="checkbox" name="combine_mutns"
           onclick="fxn_combine_mutns()" value="on" >
     </td></tr ></table>
    <div id="mwdiv" style="display:none">
     <table>
     <tr>
        <td width=350><LABEL for="multiplicative_weighting">
     &nbsp;&nbsp;&nbsp;
     :: <a class="plain" href="/static/mendel/help.html#mw" target="status"
       title="multiplicative_weighting" tabindex="119">
              fraction multiplicative effect:</a></LABEL></td>
        <td><input type="text" name="multiplicative_weighting"
                id="multiplicative_weighting"
                value="{{multiplicative_weighting}}"
                onchange="check_value(this.value,0,1)"
                title="0.0 - 1.0" accesskey="4"></td>
     </tr>  
     </table>   
     </div>
     
<div>
<hr>
<table>
     <tr>
        <td width=350><LABEL FOR="synergistic_epistasis">
                  4. <a class="plain" href="/static/mendel/help.html#se"
                    tabindex="120"
                target="status" title="synergistic_epistasis">
      Include mutation-mutation interactions (synergistic epistasis)?</a></LABEL></td>
        <td><input type="checkbox" name="synergistic_epistasis"
                   value="on" onclick="fxn_synergistic_epistasis()"
                    ></td>
        <td></td>  
     </tr>
     <tr>
        <td><LABEL for="se_nonlinked_scaling">
     &nbsp;&nbsp;&nbsp;
         a. scaling factor for non-linked SE interactions:</LABEL></td>
        <td><input type="text" name="se_nonlinked_scaling"
           value="{{se_nonlinked_scaling}}"
                   onchange="check_value(this.value,0.0,1.0)"
           title="0.0 - 1.0" ></td>
     </tr>        
     <tr>
        <td><LABEL for="se_linked_scaling">
     &nbsp;&nbsp;&nbsp;
         b. scaling factor for linked SE interactions: </LABEL></td>
        <td><input type="text" name="se_linked_scaling"
           value="{{se_linked_scaling}}"
                   onchange="check_value(this.value,0.0,1.0)"
           title="0.0 - 1.0" ></td>
     </tr>     
</table>
<hr>
<table>
     <tr>
        <td width=350><LABEL FOR="upload_mutations">
         5. <a class="plain" href="/static/mendel/help.html#upload"
               tabindex="120" target="status" title="upload_mutations">
    Upload set of custom mutations?</a> </LABEL></td>
        <td><input type="checkbox" name="upload_mutations"
                   value="on" onclick="show_hide_mutation_upload_form(1)" 
           ></td>
        <td></td>  
     </tr>
</table>
<hr>
<table>
     <tr>
        <td width=350><LABEL FOR="allow_back_mutn">
                  6. <a class="plain" href="/static/mendel/help.html#abm"
                    tabindex="120"
                target="status" title="allow_back_mutn">
    Allow back mutations?</a> </LABEL></td>
        <td><input type="checkbox" name="allow_back_mutn"
                   value="on" onclick="check_back_mutn()" ></td>
        <td></td>  
     </tr>
     </table>

</div>

</ol>
</div>
<!--*************************** SELECTION TAB *******************************-->
<div class="tab-page">
<h2 class="tab">selection</h2>
     <table>
     <tr>
        <td width=380><LABEL for="fraction_random_death">
           <ol><li><a class="plain" href="/static/mendel/help.html#frd"
                     target="status" title="fraction_random_death" tabindex="126">
            Fraction of offspring lost apart from selection ("random death"):</a></ol>
            </LABEL></td>
        <td><INPUT type="text" name="fraction_random_death"
                   value="{{fraction_random_death}}" accesskey="1"
                   onchange="check_value(this.value,0,0.99)"
                   title="0.0 - 0.99"></td>
     </tr>
     <tr>
        <td><LABEL for="heritability">
        <ol start=2><li><a class="plain" href="/static/mendel/help.html#h"
                           target="status" title="heritability" tabindex="127">
                   Heritability:</a></ol> </LABEL></td>
        <td><INPUT type="text" name="heritability" title="0 - 1"
                   onchange="check_value(this.value,0,1)"
                   accesskey="2" value="{{heritability}}"></td>
     </tr>     
     <tr>
        <td><LABEL for="non_scaling_noise">
        <ol start=3><li><a class="plain" href="/static/mendel/help.html#nsn"
                         target="status" title="non_scaling_noise"
                         tabindex="128">Non-scaling noise:</a></ol> 
            </LABEL></td>
        <td><input type="text" name="non_scaling_noise" title="0 - 1"
                   onchange="check_value(this.value,0,1)"
                   accesskey="3" value="{{non_scaling_noise}}"></td>
     </tr>     
     <tr>
        <td><LABEL for="fitness_dependent_fertility">
        <ol start=4><li><a class="plain" href="/static/mendel/help.html#fdf"
                 target="status" tabindex="128"
                 title="fitness_dependent_fertility">
                             Fitness-dependent fecundity decline?</a>
            </ol></LABEL></td> 
        <td><input type="checkbox" name="fitness_dependent_fertility"
                   accesskey="4" value="on" 1></td>
     </tr>     
     <tr>
        <td><LABEL for="selection_scheme">
        <ol start=5><li><a class="plain" href="/static/mendel/help.html#ss"
                           target="status" title="selection_scheme"
                   tabindex="128">Selection scheme:</a>
            </ol></LABEL></td>               
        <td><select NAME="selection_scheme" accesskey="5"
             onchange="fxn_selection(this.value)" >
             <option VALUE="1">Truncation selection<option SELECTED VALUE="2">Unrestricted probability selection <option VALUE="3">Strict proportionality probability selection <option VALUE="4">Partial truncation selection </select></td>
     </tr>   
     </table>
     
     <div id="ptv">
        <table>
       <tr>
          <td width=380> <LABEL for="partial_truncation_value">
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
           :: <a class="plain" href="/static/mendel/help.html#ptv"
              target="status" title="partial_truncation_value">
                partial truncation parameter, k</a></LABEL>
           <td> <input type="text" name="partial_truncation_value"
               value="{{partial_truncation_value}}" title="0.0 - 1.0"> </td>
        </tr>  
        </table>
     </div>
</div>
<!--*************************** POPULATION TAB ******************************-->
<div class="tab-page">
<h2 class="tab">population</h2>
     <table>
     
     <tr>
        <td width=380> <LABEL for="clonal_reproduction">
               1. <a class="plain" href="/static/mendel/help.html#clonal"
                 target="status" tabindex="129"
             title="clonal_reproduction">
                      Clonal reproduction?</a></LABEL> </td>
        <td> <input type="checkbox" name="clonal_reproduction"
                    value="on" onclick="fxn_clone()"
                    ></td>
     </tr>      
     </table>       
     
     <table>
     <tr>
        <td width=380> <LABEL for="clonal_haploid">
               2. <a class="plain" href="/static/mendel/help.html#ch"
                         target="status" tabindex="129"
                    title="clonal_haploid">
                      Haploid?</a> </LABEL> </td>
        <td> <input type="checkbox" name="clonal_haploid"
                    value="on" onchange="fxn_haploid()" ></td>
     </tr>      
     </table>       
     <table>
     <tr>
        <td width=380> <LABEL for="fraction_self_fertilization">
            3. <a class="plain" href="/static/mendel/help.html#fsf"
                     target="status" tabindex="129"
                       title="fraction_self_fertilization">
                      Fraction self fertilization:</a></LABEL> </td>
        <td> <input type="text" name="fraction_self_fertilization" title="0 - 1"
                    accesskey="1" value="{{fraction_self_fertilization}}"
                    onchange="check_value(this.value,0,1)"
                    style="width:5em"></td>
     </tr></table><br>
     
     <table>
     <tr>
        <td width=380> <LABEL for="dynamic_linkage">
     4. <a class="plain" href="/static/mendel/help.html#dl" target="status"
         title="dynamic_linkage" tabindex="130">
            Dynamic linkage?</a></LABEL> </td>
        <td> <input type="checkbox" name="dynamic_linkage" accesskey="2"
            value="on" onclick="fxn_dynamic_linkage()"
                CHECKED> </td>
     </tr>      
     <tr>
        <td><LABEL for="haploid_chromosome_number">
         &nbsp;&nbsp;&nbsp;
             :: haploid chromosome number:</LABEL> </td>
        <td><INPUT type="text" name="haploid_chromosome_number"
           value="{{haploid_chromosome_number}}"></td>
     </tr>     
     <tr>
        <td>&nbsp;&nbsp;&nbsp;
            <LABEL id="link_num" for="num_linkage_subunits">
                  :: number of linkage subunits:</LABEL></td>
        <td><INPUT type="text" name="num_linkage_subunits" title="1 - 10,000"
                   onchange="check_value(this.value,1,10000)"
                   value="{{num_linkage_subunits}}"></td>
     </tr>     
     </table><br>  
     
     <table>
     <tr>
        <td width=380> 
     5. <a class="plain" href="/static/mendel/help.html#pgm"
       target="status">Dynamic population size:</a><p></td>
     </tr>
     <tr>  
        <td><LABEL for="pop_growth_model">
         &nbsp;&nbsp;&nbsp;
           :: <a class="plain" href="/static/mendel/help.html#pgm"
                 target="status" title="pop_growth_model">
              population growth model:</a></LABEL> </td>
        <td><select NAME="pop_growth_model" accesskey="5"
             onchange="fxn_pop_growth_model(this.value)"  i
              >
             <option SELECTED VALUE="0">Off (fixed population size) <option VALUE="1">Exponential growth <option VALUE="2">Carrying capacity model</select></td>
     </tr>   
     <tr>
        <td><LABEL for="pop_growth_rate">
        &nbsp;&nbsp;&nbsp;
           <a id="pgr" class="plain" href="/static/mendel/help.html#pgr"
           target="status" title="pop_growth_rate" tabindex="130">
            :: population growth rate:</a></LABEL> </td>
        <td><INPUT type="text" name="pop_growth_rate"
                   onchange="check_value(this.value,1,1.26)"
               value="{{pop_growth_rate}}"></td>
     </tr>     
     </table><br>  
     
     <table>
     <tr>
        <td width=380> <LABEL for="bottleneck_yes">
     6. <a class="plain" href="/static/mendel/help.html#by" 
           target="status" title="bottleneck_yes" tabindex="132">
                Bottleneck?</a></LABEL> </td>
        <td> <input type="checkbox" name="bottleneck_yes" value="on"
                    accesskey="4"
                    onclick="fxn_bottleneck()" 
                    > </td>
     </tr></table>  
     
     <div id="bydiv" style="display:none">
     <table>
     <tr>
        <td width=380><LABEL for="bottleneck_generation" 
                             title="bottleneck_generation">
                  &nbsp;&nbsp;&nbsp;
              :: generation when bottleneck starts<br>
                  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                      <font size="-2"><em>note: negative values enable cyclic 
                                          bottlenecking</em></font></LABEL></td>
        <td><INPUT type="text" name="bottleneck_generation"
                   value="{{bottleneck_generation}}" 
                   onchange="check_bottleneck()"
                   title="2 - 50,000"></td>
     </tr>     
     <tr>
        <td><LABEL for="bottleneck_pop_size" title="bottleneck_pop_size">
               &nbsp;&nbsp;&nbsp;
               :: population size during bottleneck:</LABEL></td>
        <td><INPUT type="text" name="bottleneck_pop_size"
           value="{{bottleneck_pop_size}}"  title="2 - 1,000"></td>
     </tr>     
     <tr>
        <td><LABEL for="num_bottleneck_generations" 
                   title="num_bottleneck_generations">
               &nbsp;&nbsp;&nbsp;
               :: duration of bottleneck - generations: </LABEL></td>
        <td><INPUT type="text" name="num_bottleneck_generations"
           value="{{num_bottleneck_generations}}" title="1 - 5,000"></td>
     </tr>     
     </table>      
     </div>
     
</div>
<!--*************************** SUBSTRUCTURE TAB ****************************-->
<div class="tab-page">
<h2 class="tab">substructure</h2>

     <table>
     <tr>
        <td width=380> 
           <LABEL for="is_parallel">
          <a class="plain" href="/static/mendel/help.html#ip" 
                 target="status" title="is_parallel" tabindex="131">
          Population substructure?</a>
           </LABEL></td>
        <td> <input type="checkbox" name="is_parallel" accesskey="3"
                    onclick="fxn_is_parallel()" value="on"
                     ></td>
     </tr>      
     </table>       

     <div id="psdiv" style="display:none">

     <table>
     <tr>
        <td width=380> &nbsp;&nbsp;&nbsp;
         1. <a class="plain" href="/static/mendel/help.html#ht"
                   title="homogenous_tribes" target="status">
                      Homogeneous subpopulations?</a></td>
        <td> <input type="checkbox" name="homogenous_tribes"
                    onclick="fxn_tribes(8)" value="on" 
                    CHECKED></td>
     </tr>      
     <tr>
        <td> <LABEL for="num_tribes">
         &nbsp;&nbsp;&nbsp;
         2. <a class="plain" href="/static/mendel/help.html#nt"
               target="status" title="num_tribes">
               Number of subpopulations:</a> </LABEL></td>
        <td><input type="text" name="num_tribes" value="{{num_tribes}}" 
                   onChange="fxn_tribes(8)"
        </td>
     </tr>     
     <tr>
        <td><LABEL for="migration_model">
            &nbsp;&nbsp;&nbsp; 
            3. <a class="plain" href="/static/mendel/help.html#mm"
           target="status" title="migration_model">
           Migration model:</a></LABEL></td>
        <td><select NAME="migration_model" id="migration_model">
               <option SELECTED VALUE="1">Ring pass <option VALUE="2">Stepping-stone model<option VALUE="3">Island model
            </select>
        </td>
     </tr>

     <tr>
        <td width=380> &nbsp;&nbsp;&nbsp;
         4. <a class="plain" href="/static/mendel/help.html#mr"
                   title="migration_rate" target="status">
        Migrate
                <input type="text" name="num_indiv_exchanged"
                       title="1 to Pop Size" 
                       onchange="fxn_migration()";
                       size=2 value="{{num_indiv_exchanged}}">
                individual(s) <br> 
                &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp; &nbsp;
               
                every
                    <input type="text" name="migration_generations"
                     size=2 value="{{migration_generations}}">
                generations(s)</a></td>
    </td>
     </tr>  
     
     <tr>
        <td>&nbsp;&nbsp;&nbsp; 
            5. <a class="plain" href="/static/mendel/help.html#tc"
              target="status" title="tribal_competition">
               Competition between subpopulations?</a></LABEL></td>
        <td><input type="checkbox" name="tribal_competition" 
                    id="tribal_competition" onchange="fxn_tribes(8)"
                    value="on" 0>
        </td>
     </tr>

     <tr>
        <td>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
          a. <label id="tcsf_label">
                <a class="plain" href="/static/mendel/help.html#gssf"
                  target="status" title="tc_scaling_factor">
                  group selection scaling factor:</a></label>
        </td>
        <td> <input type="text" name="tc_scaling_factor" 
                    id="tc_scaling_factor"
                    value="{{tc_scaling_factor}}"
                    title="0 - 1." readOnly=true></td>
     </tr>

     <tr>
        <td> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          b. <label>
                <a class="plain" href="/static/mendel/help.html#gh"
                   target="status" title="group_heritability">
                   group heritability:</a> </label></td>
        <td> <input type="text" name="group_heritability" 
                    title="0 - 1
0: max noise
1: no noise"
                    onchange="check_value(this.value,0,1)"
                    value="0.2"
                    title=""></td>
     </tr>
     <tr>
        <td width=350> &nbsp;&nbsp;&nbsp;
          <LABEL FOR="tribal_fission">
          <a class="plain" href="/static/mendel/help.html#tribal_fission"
             tabindex="120" target="status" title="tribal_fission">
          6. Fission tribe?</a>
          </LABEL>
        </td>
        <td><input type="checkbox" name="tribal_fission" value="on" 
             onclick="" CHECKED></td>
        <td></td>  
     </tr>
     </table>

     <table>
     <!--
     <tr>
        <td width=350> &nbsp;&nbsp;&nbsp;
          <LABEL FOR="altruistic">
          <a class="plain" href="/static/mendel/help.html#alt"
             tabindex="120" target="status" title="altruistic">
          6. Upload altruistic mutations?</a>
          </LABEL>
        </td>
        <td><input type="checkbox" name="altruistic" value="on" 
             onclick="show_hide_mutation_upload_form(2)" ></td>
        <td></td>  
     </tr>

     <tr>
        <td width=350><LABEL FOR="social_bonus_factor">
                  <a class="plain" href="/static/mendel/help.html#sbf" 
                 target="status" title="social_bonus_factor">
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    a. social bonus scaling factor:</a> </LABEL></td>
        <td><input type="text" style="width:7em;" name="social_bonus_factor"
                   value="1.0" title="0 - 1"></td>
        <td></td>  
     </tr>
     -->
     <input type="hidden" name="social_bonus_factor" value="{{social_bonus_factor}}">

     <tr>
        <td width=380> <LABEL for="plot_avg_data">
                  <a class="plain" href="/static/mendel/help.html#pad" 
                 target="status" title="plot_avg_data">
                         &nbsp;&nbsp;&nbsp;
             7. Average subpopulation data when plotting?<br>
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                    (only effective when using Gnuplot) </LABEL></td>
        <td> <input type="checkbox" name="plot_avg_data"
                    value="on"  ></td>
     </tr>      
     </table>
      
     </div>

</div>
<!--*************************** COMPUTATION TAB *****************************-->
<div class="tab-page">
<h2 class="tab">computation</h2>
     
     <table>
     <tr>
        <td width=350> <LABEL for="auto_malloc">
             <a class="plain" href="/static/mendel/help.html#malloc" 
                target="status" title="auto_malloc">
               1. Automatically allocate memory? </td>
        <td>      <input type="checkbox" name="auto_malloc" value="on"
                   onclick="fxn_allocate_memory()" CHECKED> </a></td>
     </tr>

     <tr>
        <td align=right> 
             <a class="plain" href="/static/mendel/help.html#mtmpi" 
                target="status" title="max_del_mutn_per_indiv">
            &nbsp;&nbsp;&nbsp;  
        :: maximum deleterious mutations per individual:</a> </LABEL></td>
        <td><input type="text" name="max_del_mutn_per_indiv" accesskey="0"
               onchange="check_value(this.value,1000,5000000)" 
                   value="10000"></td>
     </tr>     

     <tr>
        <td align=right> 
             <a class="plain" href="/static/mendel/help.html#mtmpi" 
                target="status" title="max_fav_mutn_per_indiv">
            &nbsp;&nbsp;&nbsp;  
        :: maximum favorable mutations per individual:</a> </LABEL></td>
        <td><input type="text" name="max_fav_mutn_per_indiv" accesskey="0"
               onchange="check_value(this.value,1000,5000000)" 
                   value="1000"></td>
     </tr>     

     <tr>
        <td align=right> 
             <a class="plain" href="/static/mendel/help.html#mtmpi" 
                target="status" title="max_neu_mutn_per_indiv">
            &nbsp;&nbsp;&nbsp;  
        :: maximum neutral mutations per individual:</a> </LABEL></td>
        <td><input type="text" name="max_neu_mutn_per_indiv" accesskey="0"
               onchange="check_value(this.value,1000,5000000)" 
                   value="10000"></td>
     </tr>     

     <tr>
        <td width=350> <LABEL for="track_neutrals">
          2. <a class="plain" href="/static/mendel/help.html#tnm" 
                    target="status" title="track_all_mutn" tabindex="133">
                  Track all mutations? </a><br>
                  &nbsp;&nbsp;&nbsp;
                  <font size="-2">(must be checked if allele statistics 
                                   are needed)</font></td> </label>
        <td>      <input type="checkbox" name="track_all_mutn" value="on"
                   onclick="fxn_track_all_mutn()" > </td>
     </tr>
     
     <tr>
        <td width=380> <LABEL for="tracking_threshold">
           <a class="plain" href="/static/mendel/help.html#tt" 
                    target="status" title="tracking_threshold" tabindex="133">
                  &nbsp;&nbsp;&nbsp;
                    To conserve memory and speed up runs, <br>
                  &nbsp;&nbsp;&nbsp;
                    do not track mutations with fitness effects less than: </a>
             </LABEL></td>
        <td><input type="text" name="tracking_threshold" accesskey="1"
                   onchange="check_value(this.value,0,1)"
                   title="1e-4 ~ 1e-8" value="{{tracking_threshold}}">
        </td>
     </tr>   

     <tr>
        <td width=380> <LABEL for="extinction_threshold">
        <a class="plain" href="/static/mendel/help.html#et" 
               target="status" title="extinction_threshold" tabindex="133">
             3. Go extinct when mean fitness reaches: </a>
             </LABEL></td>
        <td><input type="text" name="extinction_threshold" accesskey="1"
                   onchange="check_value(this.value,0,1)"
                   title="0-1" value="{{extinction_threshold}}"></td>
     </tr>   

     <tr>
        <td width=380> <LABEL for="random_number_seed">
     4. <a class="plain" href="/static/mendel/help.html#rns" target="status" title="random_number_seed" tabindex="134">Random number generator (RNG) seed:</a> </LABEL></td>
     <td><input type="text" name="random_number_seed" title="1 - 1000"
               accesskey="2" value="{{random_number_seed}}"></td>
     </tr>
     
     <tr>
        <td width=380> <LABEL for="reseed_rng">
    &nbsp;&nbsp;&nbsp; :: <a class="plain" href="/static/mendel/help.html#reseed" 
          target="status" title="reseed_rng" tabindex="134">
          Reseed the RNG every gen using PID&#8853;Time:</a><br>
              &nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;
                  <font size="-2">(Warning: if checked, runs will not be repeatable)</font>
    </td> </label>
        <td> <input type="checkbox" name="reseed_rng" value="on"
                    onclick="" > </td>
     </tr>
     
     <tr>
        <td width=380> <LABEL for="write_dump">
     5. <a class="plain" href="/static/mendel/help.html#wd" target="status" title="write_dump" tabindex="135">Allow this run to be later re-started with new parameters? (these restart files are very large ~1GB)</a></LABEL></td>
          <td> <input type="checkbox" name="write_dump" accesskey="3"
                value="on" ></td>
     </tr>      
     
     <tr>
        <td width=350> <LABEL for="restart_case">
     6. <a class="plain" href="/static/mendel/help.html#restart" target="status" title="restart_case" tabindex="136">Restart second (third, fourth) phase of run
                with these new parameters?</a></LABEL></td>
        <td> <input type="checkbox" name="restart_case" accesskey="4"
            onclick="fxn_restart_case()" value="on" ></td>
     </tr>      
     </table>       
     
     <div id="rddiv" style="display:none">
     <table>
     <tr>
        <td width=350> <LABEL for="restart_dump_number">
        &nbsp;&nbsp;&nbsp;   :: restart from which phase of run:</LABEL></td>
        <td><input type="text" name="restart_dump_number" title="1 - 100"
               value="{{restart_dump_number}}"></td>
     </tr>     
     
     <tr>
        <td width=350> <LABEL for="restart_case_id">
        &nbsp;&nbsp;&nbsp;   :: restart from which case ID:</LABEL></td>
        <td><input type="text" name="restart_case_id"
               title="must be six letters"
                  value="{{restart_case_id}}"></td>
     </tr>        
     <tr>
        <td width=380> <LABEL for="restart_append">
     &nbsp;&nbsp;&nbsp;   :: append data to previous case:</LABEL></td>
        <td> <input type="checkbox" name="restart_append"
                value="on" CHECKED></td>
     </tr>
     </table>       
     </div>
     
     <table>
     <tr>
        <td width=380> <LABEL for="run_queue">
     7. <a class="plain" href="/static/mendel/help.html#rq"
           target="status" title="run_queue" tabindex="138">
           Queuing system:</a></LABEL></td>
        <td><select NAME= "run_queue" style="width=10em" title="hi-mem option only works on epiphany" >
            <option SELECTED VALUE="noq" >No queue<option VALUE="atq" >ATQ<option VALUE="pbs" readOnly=true>PBS<option VALUE="himem" readOnly=true>HI-MEM 
        </td>
        </select>
     </tr>
     <tr>
        <td width=380> <LABEL for="engine">
     8. <a class="plain" href="/static/mendel/help.html#cv"
               target="status">Simulation Engine:</a></LABEL></td>
        <td>
           <select NAME="engine" id="engine" >
           <option SELECTED VALUE="f" >Fortran<option VALUE="c" >C<option VALUE="j" readOnly=true>Java
           </select>   
        </td>
     </tr>
     <tr>
        <td width=380> <LABEL for="plot_allele_gens">
     9. <a class="plain" href="/static/mendel/help.html#pag"
               target="status">Compute allele frequencies every:</a></LABEL> 
        </td>
        <td> <input type="text" name="plot_allele_gens" accesskey="1" 
                    style="width:50px" 
                    onchange="check_value(this.value,0,10000)"
                    title="0-1" value="{{plot_allele_gens}}"> generations
        </td>
     </tr>
     </table>
</div>

<div class="tab-page">
<h2 class="tab">locked</h2>

<table>
<tr>
<td width=380> <LABEL for="">
          1. <a class="plain" href="/static/mendel/help.html#iha"
                   target="status" tabindex="129"
                  title="initial_heterozygous_alleles">
         Initial heterozygous alleles (ICA):</a></LABEL> </td>
</tr><tr>        
<td><LABEL for="num_contrasting_alleles">
     &nbsp;&nbsp;&nbsp;
      :: <a class="plain" href="/static/mendel/help.html#nca" 
        target="status" title="num_contrasting_alleles">
        number of initial contrasting alleles:<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
        <font size="-2">Note: fraction_recessive must be &gt; 0.0
        to work properly.</font>
        </a></LABEL> </td>
<td> <input type="text" name="num_contrasting_alleles" title="0 - 1"
        accesskey="1" value="{{num_contrasting_alleles}}"
        onchange="alpha_warning()"
        style="width:5em"  ></td>
</tr><tr>       
<td><LABEL for="max_total_fitness_increase">
     &nbsp;&nbsp;&nbsp;
     :: <a class="plain" href="/static/mendel/help.html#mtfi"
       target="status" title="max_total_fitness_increase">
       maximum total fitness increase:</a></LABEL> <br>
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
       <font size="-2">Note: this value must be &gt; 0 for ICA to work.</font>
       
       </td>
<td> <input type="text" name="max_total_fitness_increase" title="0 - 1"
        accesskey="1" value="{{max_total_fitness_increase}}"
        onchange="check_value(this.value,0,1)"
        style="width:5em"  ></td>
</tr>       
     <tr>
    <td><LABEL for="">
        <a class="plain" href="/static/mendel/help.html#fomb" 
           target="status">
              2. Include neutrals in analysis:</a> 
            </LABEL></td>
        <td><input type="checkbox" name="track_neutrals" 
                   title="" onclick="fxn_track_neutrals()" ></td>
        <td></td>
     </tr>
     <tr>
        <td><LABEL for="fraction_neutral">
       &nbsp;&nbsp;&nbsp;    
              <a class="plain" href="/static/mendel/help.html#fmun" 
                 target="status" title="fraction_neutral" tabindex="">
              :: fraction of genome which is non-functional <em>junk</em>:</a> 
        </LABEL> </td>
        <td><INPUT type="text" name="fraction_neutral" id="fmun" accesskey="1"
                   value="{{fraction_neutral}}"
                   onchange="compute_u();fxn_fraction_neutral()"
                   title="0 - 1"></td>
     </tr>     
     <tr>
    <td><LABEL for="uneu">
       &nbsp;&nbsp;&nbsp; <a class="plain" 
                                 href="/static/mendel/help.html#fomb" 
                                 target="status">
            <font color="grey">:: neutral mutation rate:</font></a> 
            </LABEL></td>
    <td><INPUT name="uneu" type="text" readOnly=true></td>
        <td></td>
     </tr>
     <tr>
    <td><LABEL for="polygenic_beneficials">
        <a class="plain" href="/static/mendel/help.html#pbe" 
           target="status">
              3. Polygenic beneficial effects?</a> 
            </LABEL></td>
        <td><input type="checkbox" name="polygenic_beneficials" 
                   title="" onclick="fxn_polygenic_beneficials()" 
           ></td>
        <td></td>
     </tr>
     <tr>
        <td><LABEL for="polygenic_threshold">
       &nbsp;&nbsp;&nbsp;    
              <a class="plain" href="/static/mendel/help.html#pbnr" 
                 target="status" title="polygenic_threshold" tabindex="">
              :: How many independent mutations are needed to get a beneficial
             effect:</a> 
        </LABEL> </td>
        <td><INPUT type="text" name="polygenic_threshold" id="pbnr" accesskey="1"
                   value="{{polygenic_threshold}}"
                   onchange=""
                   title="1 - 3"></td>
     </tr>     
     <tr>
        <td><LABEL for="polygenic_match_criteria">
       &nbsp;&nbsp;&nbsp;    
              <a class="plain" href="/static/mendel/help.html#pbnr" 
                 target="status" title="polygenic_match_criteria" tabindex="">
              :: How many digits need to be the same in order for mutations 
             to be considered equal:</a> 
        </LABEL> </td>
        <td><INPUT type="text" name="polygenic_match_criteria" 
               id="pbnr" accesskey="1"
                   value="{{polygenic_match_criteria}}"
                   onchange=""
                   title="1 - 3"></td>
     </tr>     
</table>
</div>

</div>
</div>

<div id="upload_mutations_div" style="display:none" align="center">
<fieldset style="background-color: white">
<legend>Upload Mutations</legend>

     <table>
     <tr>
<!--
        <td width=350><LABEL FOR="mutn_file_id">
                  <a class="plain" href="/static/mendel/help.html#mfid" 
                 id="mutn_file_id_label" tabindex="120"
                 target="status" title="mutn_file_id">
    File id of mutations file:</a> </LABEL></td>
-->
        <td><input type="hidden" name="mutn_file_id" style="width:7em;"
                   value=""
                   title="Currently this filename cannot be changed" 
                   readOnly="true"></td>
        <td></td>  
     </tr>
     </table>

<font size="+1">
     <a href="/static/mendel/upload_mutations.xlsx">download worksheet</a> ::
     <label name="upload_mutn_link"><a href="javascript:cid=dmi.case_id.value;popUp('mutn_upload.pl?run_dir=/Library/WebServer/Documents/mendel_user_data&user_id=wes&case_id=' + cid + '&mutn_file_id=',600,600);">upload mutations</a></label> ::
     <label name="upload_mutn_link"><a href="javascript:cid=dmi.case_id.value;mfid=dmi.mutn_file_id.value;popUp('more.pl?user_id=wes&case_id='+cid+'&file_name='+mfid+'&nothing=',600,600);">view mutations</a></label> 
</font>
</fieldset>
</div>

<font color="red" size="+1"> <div align=center id="note_to_user"> </div> </font> 
<input type="hidden" name="version" value="2.2.5">
<input type="hidden" name="quota" value="16384">
<input type="hidden" name="run_dir" value="/Library/WebServer/Documents/mendel_user_data">

</form>

<script language="Javascript">dmi = document.mendel_input</script>
<script language="Javascript">fxn_synergistic_epistasis_disable();</script>
<script language="Javascript">document.getElementById("ptv").style.display = "none";</script>
<script language="Javascript">dmi.pop_growth_rate.readOnly = false;</script>
</body></html>
