function fxn_init() {
   fxn_tribes(8);
   fxn_fitness_distrib_type_init();
   //fxn_selection_init();
   // assign values that were parsed from input file to JS vars
   // we need to store these, in case we need access them later
   tracking_threshold = dmi.tracking_threshold.value;
   fraction_neutral = dmi.fraction_neutral.value;
   compute_u();

   // properly grey out items
   fxn_allocate_memory();
   fxn_combine_mutns_able();
   fxn_dynamic_linkage_able();
   fxn_bottleneck_able();
   fxn_restart_case_able();
   fxn_is_parallel();
   fxn_migration();
   fxn_clone();
   fxn_fraction_neutral();
   fxn_polygenic_beneficials();
   fxn_track_neutrals();
   fxn_track_all_mutn();
   fxn_init_tracking_threshold();
   show_hide_mutation_upload_form();
   //document.getElementById("tribediv").style.display = "none";
   dmi.case_id.focus();
   // this is in tabpane.js
   setupAllTabs();
}

function fxn_set_caseid() {
        parent.frames.contents.caseidform.case_id.value = 
           dmi.case_id.value;
}

function set_random_caseid() {
        var c; var n;
        //var s=65; n=25; //for all caps
        var s=97; n=25;   //for all lowercase
        c = ''
        for (var i=0; i<6; i++) { 
           c += String.fromCharCode(s + Math.round(Math.random() * n));
        }
        dmi.case_id.value = c;
}

function fxn_set_this_caseid() {
    dmi.case_id.focus();
        // get string from control panel
        var a = parent.frames.contents.caseidform.case_id.value;
        // get just the case_id (in case of format uid/caseid)
        var b = a.substring(a.length-6);
        // get the last three characters
        var c = b.substring(3);
        c = String.fromCharCode(97 + Math.round(Math.random() * 25));
        c += String.fromCharCode(97 + Math.round(Math.random() * 25));
        c += String.fromCharCode(97 + Math.round(Math.random() * 25));
        var d = b.substring(0,3); 
        var e = d + c;
        if(dmi.caseid_cb.checked) {
           if(dmi.case_id.value == "") {
              set_random_caseid();
              dmi.case_id.select();
           } else {
              dmi.case_id.value = e;
           }          
        } else {
           dmi.case_id.value = "";
        }
}

function fxn_opf(x, min, max) {
   var opf = 2*x;
   status("offspring_per_female = " + opf);
   check_value(x, min, max);
}

function alpha_warning() {
   status("WARNING: this function is experimental and largely untested.");
}

function check_value(x, min, max) {
   // make sure values are numbers not strings
   min *= 1;
   max *= 1;
   if(x < min || x > max || isNaN(x)) {
      alert("WARNING: Value must be between " + min + " and " + max);
      // status("WARNING: Value must be between " + min + " and " + max );
   }
}

function fxn_synergistic_epistasis() {
        fxn_synergistic_epistasis_able();
        if(dmi.synergistic_epistasis.checked) {
       if (dmi.se_nonlinked_scaling.value = "0.0"){
              dmi.se_nonlinked_scaling.value = "0.1";
           }
        }
}

function fxn_synergistic_epistasis_able() {
    if(dmi.synergistic_epistasis.checked) {
           dmi.se_nonlinked_scaling.disabled = false;
           dmi.se_linked_scaling.disabled = false;
    } else {
       dmi.se_nonlinked_scaling.disabled = true;
       dmi.se_linked_scaling.disabled = true;
    }
}
function fxn_synergistic_epistasis_disable() {
        dmi.se_nonlinked_scaling.disabled = true;
        dmi.se_linked_scaling.disabled = true;
}

function fxn_combine_mutns() {
        fxn_combine_mutns_able();
    if (dmi.combine_mutns.checked) {
        dmi.multiplicative_weighting.value = 0.5;
        dmi.multiplicative_weighting.select();
            window.scrollBy(0,50);
    } else {
        dmi.multiplicative_weighting.value = 0.0;
    }
}
function fxn_combine_mutns_able() {
   if (dmi.combine_mutns.checked) {
    document.getElementById("mwdiv").style.display = "block";
   } else {
    document.getElementById("mwdiv").style.display = "none";
   }
}

function fxn_dynamic_linkage() {
        fxn_dynamic_linkage_able();
    if (dmi.dynamic_linkage.checked) {
        //mendel_input.num_linkage_subunits.value = 1000;
                if (dmi.haploid_chromosome_number.value = "0")
               dmi.haploid_chromosome_number.value = "23";
    } else {
        //dmi.num_linkage_subunits.value = 1000;
    }
}
function fxn_dynamic_linkage_able() {
    if (dmi.dynamic_linkage.checked) {
       dmi.haploid_chromosome_number.disabled = false;
           document.getElementById("link_num").innerText = 
            ":: number of linkage subunits:";
    } else {
       dmi.haploid_chromosome_number.disabled = true;
       document.getElementById("link_num").innerText = 
            ":: fixed block linkage number:";
    }
}

function fxn_haploid() {
   if (dmi.clonal_haploid.checked) {
      dmi.fraction_recessive.value = 0.0; 
      dmi.dominant_hetero_expression.value = 1.0; 
      status("Setting fraction_recessive to 0 and dominant_hetero_expression to 1");
   } else {
      dmi.dominant_hetero_expression.value = 0.5; 
      status("Setting dominant_hetero_expression back to 0.5");
   }
}

function fxn_is_parallel() {
   if (dmi.is_parallel.checked) {
      document.getElementById("psdiv").style.display = "block";
      window.scrollBy(0,500);
      //document.getElementById("engine").selectedIndex = 1;
      //status("NOTE: Changed engine to C");
      //dmi.fraction_neutral.value = 0;
      //status("Setting fraction_neutral to 0. Neutral mutations not supported in parallel runs.");
   } else {
      document.getElementById("psdiv").style.display = "none";
      status("");
   }
}

function status(msg) {
      //omsg = document.getElementById("note_to_user").innerText;
      //mymsg = omsg + msg;
      mymsg = msg;
      document.getElementById("note_to_user").innerText = mymsg;
}

function fxn_restart_case() {
        fxn_restart_case_able();
    if (dmi.restart_case.checked) {
            if (dmi.restart_dump_number.value = "0") {
                dmi.restart_dump_number.value = "1";
            } 
    }
}

function fxn_restart_case_able() {
   if (dmi.restart_case.checked) {
      document.getElementById("rddiv").style.display = "block";
   } else {
      document.getElementById("rddiv").style.display = "none";
   }
}

function fxn_bottleneck() {
        fxn_bottleneck_able();
    if (dmi.bottleneck_yes.checked) {
                if (dmi.bottleneck_generation.value = "0") {
                    dmi.bottleneck_generation.value = "1000";
                    window.scrollBy(0,500);
                }
                if (dmi.bottleneck_pop_size.value = "0") {
                    dmi.bottleneck_pop_size.value = "100";
                }
                if (dmi.num_bottleneck_generations.value = "0") {
                    dmi.num_bottleneck_generations.value = "500";
                }
    }
}
function fxn_bottleneck_able() {
   if (dmi.bottleneck_yes.checked) {
      document.getElementById("bydiv").style.display = "block";
   } else {
      document.getElementById("bydiv").style.display = "none";
   }
}

function check_bottleneck() {
   bgen = dmi.bottleneck_generation.value;
   if(bgen < 0) {
     status("Cyclic bottlenecking turned on");
     if(dmi.num_bottleneck_generations.value > -bgen ) {
         dmi.num_bottleneck_generations.value = -bgen - 1; 
     }
   } else {
     status("Cyclic bottlenecking turned off");
   }
}

function fxn_allocate_memory() {
    if (dmi.auto_malloc.checked) {
           dmi.max_del_mutn_per_indiv.disabled = true;
           dmi.max_neu_mutn_per_indiv.disabled = true;
           dmi.max_fav_mutn_per_indiv.disabled = true;
           status("");
        } else {
           dmi.max_del_mutn_per_indiv.disabled = false;
           dmi.max_neu_mutn_per_indiv.disabled = false;
           dmi.max_fav_mutn_per_indiv.disabled = false;
           dmi.max_del_mutn_per_indiv.select();
        }
}

function compute_u() {
   u = dmi.mutn_rate.value;
   uneu = dmi.uneu.value = u*dmi.fraction_neutral.value;
   dmi.uben.value = (u-uneu)*dmi.frac_fav_mutn.value;
   dmi.udel.value = (u-uneu)*(1-dmi.frac_fav_mutn.value);
   dmi.uneu.value = uneu;
}

function fxn_fraction_neutral() {
   if(dmi.fraction_neutral.value>0) {
      dmi.track_neutrals.checked = true;
      //status("tracking all mutations");
   } else {
      dmi.track_neutrals.checked = false;
      //status("not tracking all mutations");
   }      
   compute_u();
}

function fxn_polygenic_beneficials() {
   if(dmi.polygenic_beneficials.checked) {
      dmi.track_neutrals.checked = true
      fxn_track_neutrals()
      dmi.fraction_neutral.value = 1.0
      dmi.frac_fav_mutn.value = 0.0
      compute_u();
      status("setting on track_neutrals, setting fraction_neutral = 1.0")
   }
}

function fxn_track_neutrals() {
   if(dmi.track_neutrals.checked) {
      dmi.fraction_neutral.disabled = false;
      if ( fraction_neutral > 0 ) {
         dmi.fraction_neutral.value = fraction_neutral;
      } else {
         dmi.fraction_neutral.value = 0.9;
      }
      // Modify mutation rate -- divide by fraction_neutrals
      //dmi.mutn_rate.value = Math.round(dmi.mutn_rate.value/(1-dmi.fraction_neutral.value));
      dmi.fraction_neutral.select();
      dmi.track_all_mutn.checked = true;
      fxn_track_all_mutn();
      document.getElementById("mutn_rate").innerText = "Total mutation rate per individual per generation:";
      status("including neutrals in analysis will require more memory and will slow run, and all mutations will be tracked");
   } else {
      // Modify mutation rate -- multiply by fraction_neutrals
      //dmi.mutn_rate.value = Math.round(dmi.mutn_rate.value*(1-dmi.fraction_neutral.value));
      document.getElementById("mutn_rate").innerText = "Total non-neutral mutation rate per individual per generation:";
      dmi.fraction_neutral.value = 0.0;
      dmi.fraction_neutral.disabled = true;
      status("");
   }
   compute_u();
}

function fxn_track_all_mutn() {
   if(dmi.track_all_mutn.checked) {
      dmi.tracking_threshold.value = 0;
      dmi.tracking_threshold.disabled = true;
   } else {
      dmi.tracking_threshold.disabled = false;
      dmi.tracking_threshold.value = tracking_threshold;
      dmi.tracking_threshold.select();
      dmi.track_neutrals.checked = false;
   }
}

function fxn_init_tracking_threshold() {
   if(dmi.tracking_threshold.value == 0) {
      dmi.track_all_mutn.checked = true;
   } else {
      dmi.track_all_mutn.checked = false;
   } 
   // set a default tracking_threshold value, in case user
   // is not restarting from a file that has a specified tracking 
   // threshold value.
   if(tracking_threshold == 0) { tracking_threshold = 1.e-5; }
}

function fxn_fitness_distrib_type_init() {
   fdt = dmi.fitness_distrib_type.value;
   // equal effect distribution
   if (fdt == 0) {
      document.getElementById("ufe_div").style.display = "block";
      document.getElementById("weibull_div").style.display = "none";
      document.getElementById("crdiv").style.display = "block";
      dmi.combine_mutns.disabled = false;
      dmi.synergistic_epistasis.disabled = false;
      window.scrollBy(0,500);
   // Weibull distribution
   } else if (fdt == 1) {
      document.getElementById("ufe_div").style.display = "none";
      document.getElementById("weibull_div").style.display = "block";
      document.getElementById("crdiv").style.display = "block";
      dmi.combine_mutns.disabled = false;
      dmi.synergistic_epistasis.disabled = false;
      window.scrollBy(0,500);
   // All Neutral
   } else if (fdt == 2) {
      document.getElementById("ufe_div").style.display = "none";
      document.getElementById("weibull_div").style.display = "none";
      document.getElementById("crdiv").style.display = "none";
      dmi.combine_mutns.disabled = true;
      dmi.synergistic_epistasis.disabled = true;
      fxn_disable_synergistic_epistasis();
      window.scrollBy(0,500);
   // Bi-modal
   } else if (fdt == 3) {
      document.getElementById("ufe_div").style.display = "block";
      document.getElementById("weibull_div").style.display = "block";
      document.getElementById("crdiv").style.display = "block";
      dmi.combine_mutns.disabled = false;
      dmi.synergistic_epistasis.disabled = false;
      window.scrollBy(0,500);
   } else {
      document.getElementById("ufe_div").style.display = "none";
      document.getElementById("weibull_div").style.display = "block";
      document.getElementById("crdiv").style.display = "block";
      dmi.combine_mutns.disabled = false;
      dmi.synergistic_epistasis.disabled = false;
   }
}

function fxn_fitness_distrib_type_change() {
   fxn_fitness_distrib_type_init();
   fdt = dmi.fitness_distrib_type.value;
   if (fdt == 0) {
      dmi.dominant_hetero_expression.value = 1.0;
   } else {
      dmi.dominant_hetero_expression.value = 0.5;
   }
}

function show_hide_advanced() {
    if (dmi.advsel.checked) {
           document.getElementById("tab-pane-1").style.display = "block";
           window.scrollBy(0,500);
        } else {
           document.getElementById("tab-pane-1").style.display = "none";
        }
}

function show_hide_parser() {
    if (document.parsed_data.show_data.checked) {
           document.getElementById("parser").style.display = "block";
           //window.scrollBy(0,500);
        } else {
           document.getElementById("parser").style.display = "none";
        }
}

function show_hide_mutation_upload_form(i) {
        // if user checks upload mutations on the mutation pane
        // then automatically also check the upload mutations box
        // under population substructure, and vice-versa
        if(i==2) {
           if (dmi.altruistic.checked) {
              dmi.upload_mutations.checked = true;
           } else {
              dmi.upload_mutations.checked = false;
           }
        }

        // if user checks upload mutations on the mutation pane
        // then automatically also check the upload mutations box 
        // under population substructure, and vice-versa
    if (dmi.upload_mutations.checked) {
           document.getElementById("upload_mutations_div").style.display = "block";
           //dmi.mutn_file_id.disabled = false;
           window.scrollBy(0,500);
        } else if (dmi.altruistic.checked) {
           document.getElementById("upload_mutations_div").style.display = "block";
        } else {
          document.getElementById("upload_mutations_div").style.display = "none";
          //dmi.mutn_file_id.disabled = true;
        }
}

function fxn_migration() {
   x = parseInt(1*dmi.num_indiv_exchanged.value);
   max = parseInt(1*dmi.pop_size.value);
   if(x == 0) {
      dmi.migration_generations.disabled = true;
   } else {
      dmi.migration_generations.disabled = false;
      //dmi.migration_generations.value = 1;
      if(x > max || x < 0) alert("Value must be between 0 and " + max);
   }
   dmi.num_indiv_exchanged.value = x;
}

function fxn_tribes(max_tribes) {
   myobject = dmi.num_tribes;
   num_tribes = myobject.value;

   // set max number of tribes for server from setting in config.inc
   if(num_tribes > max_tribes) { 
      myobject.value = max_tribes;
      num_tribes = max_tribes;
   }
   // set min number of tribes 
   if(num_tribes < 2) {
      myobject.value = 2; 
      num_tribes = 2;
   }

   if (dmi.homogenous_tribes.checked) {
      document.getElementById("tribediv").style.display = "none";
   } else {
      document.getElementById("tribediv").style.display = "block";
   }

   if (dmi.tribal_competition.checked) {
      dmi.tc_scaling_factor.disabled = false;
      dmi.group_heritability.disabled = false;
      dmi.tc_scaling_factor.select();
      status("Group competition is still under development. Proceed with caution. Must set extinction threshold > 0 for tribal fission.");
      if(dmi.extinction_threshold.value == 0.0)  {
         dmi.extinction_threshold.value = 0.1;
      }
   } else {
      dmi.tc_scaling_factor.disabled = true;
      dmi.group_heritability.disabled = true;
      status("");
   }

   dmi.num_tribes.title = "2 - " + max_tribes;
   // Add options to tribe_id select statement
   dmi.tribe_id.options.length=0;
   for (i = 0; i < num_tribes; i++) {
      a = (i+1)/1000 + ''; // compute number of tribe as a string
      b = a.substring(1);  // remove the leading 0 from 0.001, 0.002, etc.
      if((i+1)%10==0) b += '0'; // every 10 tribes: 0.01->0.010, 0.02->0.020, etc.
      dmi.tribe_id.options[i]=new Option(b, b, true, false);
   }
}

function fxn_clone() {
   if (dmi.clonal_reproduction.checked) {
      dmi.fraction_self_fertilization.disabled = true;
      dmi.num_contrasting_alleles.disabled = true;
      dmi.max_total_fitness_increase.disabled = true;
      dmi.dynamic_linkage.disabled = true;
      dmi.haploid_chromosome_number.disabled = true;
      dmi.num_linkage_subunits.value = 1;
   } else {
      dmi.fraction_self_fertilization.disabled = false;
      dmi.num_contrasting_alleles.disabled = false;
      dmi.max_total_fitness_increase.disabled = false;
      dmi.dynamic_linkage.disabled = false;
      dmi.haploid_chromosome_number.disabled = false;
      //dmi.num_linkage_subunits.value = 1000;
   }
}

function fxn_selection_init() {
  i = dmi.selection_scheme.value;
  if (i == 1 || i == 2 || i == 4) {
     dmi.non_scaling_noise.value = 0.05;
     //status("Setting non_scaling_noise to 0.05");
  } else {
     dmi.non_scaling_noise.value = 0.0;
     //status("Setting non_scaling_noise to 0.0");
  } 
}

function fxn_selection(i) {
  fxn_selection_init();
  if (i == 4) {
     document.getElementById("ptv").style.display = "block";
     dmi.partial_truncation_value.select();
  } else {
     document.getElementById("ptv").style.display = "none";
  } 
}

function check_back_mutn() {
   if(dmi.allow_back_mutn.checked) {
      tt = dmi.tracking_threshold.value;
      dmi.tracking_threshold.value = "0.0";
      status("NOTE: Changed tracking threshold to 0.0 so that all mutations will be tracked");
   } else {
      if(tt<=0) tt = 1.e-5; 
      dmi.tracking_threshold.value = tt;
      status("NOTE: Changed tracking threshold back to " + tt );
   }
}

function fxn_pop_growth_model(i) {
  // the Fortran engine does not support dynamic population sizes
  // so change the engine if dynamic population is turned on
  //if(i == 1 || i == 2) {
  //   document.getElementById("engine").selectedIndex = 1;
  //   status("NOTE: Changed simulation engine to C");
  //}
  if (i == 0) {
     dmi.pop_growth_rate.disabled = true;
     document.getElementById("gen").innerText =
                        "Generations:";
     document.getElementById("pop").innerText =
                        "Population size (per subpopulation):";
     status("");
  } else if (i == 1) {
     dmi.pop_growth_rate.disabled = false;
     document.getElementById("pgr").innerText =
                        "    :: intrinsic growth rate:";
     document.getElementById("gen").innerText =
                        "Max population size:";
     document.getElementById("pop").innerText =
                        "Starting population size (per subpopulation):";
     dmi.pop_size.value = "2"; 
     dmi.num_generations.value = "2000"; 
     dmi.pop_growth_rate.value = "1.01"; 
     dmi.pop_growth_rate.title = "1.00 - 1.26"; 
     status("WARNING: dynamic populations are experimental and largely untested");
  } else if (i == 2) {
     dmi.pop_growth_rate.disabled = false;
     document.getElementById("pgr").innerText =
                        "    :: maximum reproductive rate of an individual:";
     document.getElementById("gen").innerText =
                        "Carrying capacity:";
     document.getElementById("pop").innerText =
                        "Starting population size (per subpopulation):";
     dmi.pop_size.value = "2"; 
     dmi.num_generations.value = "1000"; 
     dmi.pop_growth_rate.value = "0.1"; 
     dmi.pop_growth_rate.title = "0.0 - 1.0"; 
     status("WARNING: dynamic populations are experimental and largely untested");
  } else {
     dmi.pop_growth_rate.disabled = false;
     status("");
  }

}
