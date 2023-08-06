attributes:
###########
    age:
        values: [kid, adult, old]
        shares: [17%, 60%,   23%]                 # numbers can be written in decimal, percentage or exponential notation

    risk:
        values: [high, moderate, low]
        shares:
            for age=kid: [5%, %%, 70%]            # '%%' stands for the rest to reach 100%
            for age=old: [60%, %%, 8%]
            otherwise:   [18%, %%, 20%]

    state:
        values: [susceptible, exposed, asymptomatic, presymptomatic, symptomatic, hospitalized, dead, recovered]
        shares: [%%,          1E-5,    0,            0,              0,           0,            0,    0]                                                             

    quarantined:
        values: [yes, no, was]                    # the 'was' value helps to calculate incidence rates, since quarantined are the registered 
                                                  # cases and new infections are changes in the set (quarantined in [yes,was])
        shares: [0,   1,  0]


progressions:
#############
    incubation:
        # exposed people getting infectious some (age-dependent) time after exposure
        for state=exposed:
            after.fix(latency_period):                      # progression happens after fixed time
                set state=
                    asymptomatic: asymptomatic_share
                    presymptomatic: 1 - asymptomatic_share

    symptoms_start:
        # presymptomatic people becoming symptomatic after some time
        for state=presymptomatic:
            after.std(2.13, 1.5):                 # normal distribution of progression time (mu, sigma)
                set state=symptomatic

    recover_from_asymptomatic:
        # asymptomatic cases recover after a while
        for state=asymptomatic:
            after.std(7,2.5):
                set state=recovered
                
    symptoms_worsen:
        # symptomatic people go to hospital or recover
        for state=symptomatic:
            prob_hospital = 
                for risk=high: 70%
                for risk=moderate: 25%
                for risk=low: 5%
            for prob_hospital:
                after.std(5, 3):
                    set state=hospitalized
                    set quarantined=yes
            otherwise:
                after.std(3.6, 2):
                    set state=recovered            

    in_hospital_recover_or_die:
        # hospitalized people either die or recover (within different times)
        for state=hospitalized:
            prob = 
                for risk=high: 70%
                for risk=moderate: 25%
                for risk=low: 5%
            for prob:
                duration = 
                    for age=kid: 10
                    for age=adult: 30
                    for age=old: 7
                after.std(duration, duration/2):
                    set state=dead
            otherwise:
                duration = 
                    for age=kid: 5
                    for age=adult: 10
                    for age=old: 3
                after.std(duration, duration/2):
                    set state=recovered            

    infection:
        # susceptible people become exposed
        for state=susceptible:                 
            for infection_probability:
                set state=exposed
                for 50%:
                    set quarantined=yes

    handle_quarantine:
        #infection is reported, people are put in quarantine. Recovered or dead people are no longer quarantined
        for quarantined=no:
            for state=exposed:
                for 1%:                           # extremely low daily probability to register
                    set quarantined=yes
            for state in [asymptomatic, presymptomatic]:
                for 3%:                           # low daily probability to register
                    set quarantined=yes
            for state=symptomatic:
                for 25%:                          # high probability to have an official test result
                    set quarantined=yes
        for quarantined=yes:
            for state in [recovered, dead]:
                set quarantined=was

parameters:
###########
    latency_period: 5
    asymptomatic_share: 18.4%      #how many infections will remain asymptomatic 
    f_asymptomatic : 0.231         #factor for infectiousness relative to symptomatic
    f_presymptomatic : 0.692       #factor for infectiousness relative to symptomatic
    factor_when_quarantined : 0.05 #factor for infectiousness relative to unquarantined
    
    contacts_kid_kid : 10          #daily contact frequency between age groups
    contacts_kid_adult : 4
    contacts_kid_old : 1
    contacts_adult_adult : 5
    contacts_adult_old : 1.5
    contacts_old_old : 3

    infections_per_contact : 0.5   #transmission probability given a contact to (fully) infectious person 
    
formulas:
#########
    # name population segments by age (just a shortcut to make subsequent formulas more readable
    Kids: ALL with age=kid
    Adults: ALL with age=adult
    Olds: ALL with age=old

    # (fully) infected people within partial population X, asymtomatic/presymptomatic cases count less
    infected(X): $(X with state=symptomatic) + f_asymptomatic*$(X with state=asymptomatic) + f_presymptomatic*$(X with state=presymptomatic)

    # force of infection within X, treating quarantined people as less infectious
    force(X): infected(X with quarantined=no) + factor_when_quarantined * infected(X with quarantined=yes)

    # force of infection corresponds to (age-specific) contacts to (age-specific) infection rates 
    force_of_infection: 
        for age=kid: contacts_kid_kid * force(Kids) + contacts_kid_adult * force(Adults) + contacts_kid_old * force(Olds)
        for age=adult: contacts_kid_adult * force(Kids) + contacts_adult_adult * force(Adults) + contacts_adult_old * force(Olds)
        for age=old: contacts_kid_old * force(Kids) + contacts_adult_old * force(Adults) + contacts_old_old * force(Olds)

    # infection probability is the force of infection scaled by overall transmission probability
    infection_probability: infections_per_contact * force_of_infection
    
    # new infections during the last d days
    NewInfections(X,d): $(X with quarantined in [yes,was]) - $(X.before(d) with quarantined in [yes,was])

results:
########
    # all attribute value shares are returned automatically. This section only adds specific values (as time series)
    r: NewInfections(ALL,4)/NewInfections(ALL.before(4), 4)
    incidence7 : 100000 * NewInfections(ALL,7)
    dailynew: 83000000 * NewInfections(ALL,1)
