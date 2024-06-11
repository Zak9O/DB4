"""
    HOW TO USE
    First initialize the temperature sensors
    Then you can pass the sensors to the read_temp function
"""

from machine import Pin
from machine import ADC
from machine import DAC
from math import log

import machine
import utime

adc_V_lookup = [0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9758824, 0.9944118, 0.957353, 0.9388236, 0.8338236, 0.7782353, 0.8708824, 0.6794118, 0.5991177, 0.5682353, 0.7782353, 0.4632353, 0.4138236, 0.6979412, 0.2964706, 0.2408824, 0.1914706, 0.5991177, 0.09264707, 0.0432353, 1.087059, 1.090147, 1.093235, 1.096324, 1.099412, 1.1025, 1.105588, 1.108677, 1.111765, 1.114853, 1.117941, 1.121029, 1.124118, 1.127206, 1.130294, 1.133382, 1.136471, 1.139559, 1.142647, 1.145735, 1.148824, 1.152941, 1.157059, 1.161177, 1.164265, 1.167353, 1.170441, 1.17353, 1.177647, 1.181765, 1.185882, 1.188353, 1.190824, 1.193294, 1.195765, 1.198235, 1.202353, 1.206471, 1.210588, 1.213676, 1.216765, 1.219853, 1.222941, 1.226029, 1.229118, 1.232206, 1.235294, 1.239412, 1.243529, 1.247647, 1.250118, 1.252588, 1.255059, 1.257529, 1.26, 1.264118, 1.268235, 1.272353, 1.278529, 1.284706, 1.286471, 1.288235, 1.29, 1.291765, 1.29353, 1.295294, 1.297059, 1.300147, 1.303235, 1.306324, 1.309412, 1.3125, 1.315588, 1.318676, 1.321765, 1.324853, 1.327941, 1.331029, 1.334118, 1.337206, 1.340294, 1.343382, 1.346471, 1.349559, 1.352647, 1.355735, 1.358824, 1.361912, 1.365, 1.368088, 1.371176, 1.375294, 1.379412, 1.383529, 1.386618, 1.389706, 1.392794, 1.395882, 1.4, 1.404118, 1.408235, 1.411324, 1.414412, 1.4175, 1.420588, 1.423676, 1.426765, 1.429853, 1.432941, 1.436029, 1.439118, 1.442206, 1.445294, 1.448382, 1.451471, 1.454559, 1.457647, 1.460735, 1.463824, 1.466912, 1.47, 1.474118, 1.478235, 1.482353, 1.485441, 1.488529, 1.491618, 1.494706, 1.497177, 1.499647, 1.502118, 1.504588, 1.507059, 1.511177, 1.515294, 1.519412, 1.5225, 1.525588, 1.528677, 1.531765, 1.534853, 1.537941, 1.541029, 1.544118, 1.546588, 1.549059, 1.551529, 1.554, 1.556471, 1.560588, 1.564706, 1.575, 1.577059, 1.585294, 1.593529, 1.596, 1.598471, 1.600941, 1.603412, 1.605882, 1.608971, 1.612059, 1.615147, 1.618235, 1.622353, 1.626471, 1.630588, 1.633059, 1.635529, 1.638, 1.640471, 1.642941, 1.647059, 1.651177, 1.655294, 1.658382, 1.661471, 1.664559, 1.667647, 1.670735, 1.673824, 1.676912, 1.68, 1.684118, 1.688235, 1.692353, 1.694412, 1.696471, 1.698529, 1.700588, 1.702647, 1.704706, 1.707794, 1.710882, 1.713971, 1.717059, 1.720147, 1.723235, 1.726324, 1.729412, 1.733529, 1.737647, 1.741765, 1.744853, 1.747941, 1.751029, 1.754118, 1.757206, 1.760294, 1.763382, 1.766471, 1.770588, 1.774706, 1.778824, 1.781912, 1.785, 1.788088, 1.791177, 1.794265, 1.797353, 1.800441, 1.80353, 1.807647, 1.811765, 1.815882, 1.818971, 1.822059, 1.825147, 1.828235, 1.830706, 1.833177, 1.835647, 1.838118, 1.840588, 1.843677, 1.846765, 1.849853, 1.852941, 1.857059, 1.861177, 1.865294, 1.868382, 1.871471, 1.874559, 1.877647, 1.880735, 1.883824, 1.886912, 1.89, 1.893088, 1.896177, 1.899265, 1.902353, 1.90647, 1.910588, 1.914706, 1.917794, 1.920882, 1.923971, 1.927059, 1.931176, 1.935294, 1.939412, 1.941882, 1.944353, 1.946824, 1.949294, 1.951765, 1.954853, 1.957941, 1.96103, 1.964118, 1.970294, 1.976471, 1.979559, 1.982647, 1.985735, 1.988824, 1.991294, 1.993765, 1.996235, 1.998706, 2.001177, 2.005294, 2.009412, 2.01353, 2.016618, 2.019706, 2.022794, 2.025882, 2.028971, 2.032059, 2.035147, 2.038235, 2.041324, 2.044412, 2.0475, 2.050588, 2.053677, 2.056765, 2.059853, 2.062941, 2.067059, 2.071177, 2.075294, 2.077765, 2.080235, 2.082706, 2.085176, 2.087647, 2.091765, 2.095882, 2.1, 2.106177, 2.112353, 2.114118, 2.115882, 2.117647, 2.119412, 2.121176, 2.122941, 2.124706, 2.127794, 2.130883, 2.133971, 2.137059, 2.141176, 2.145294, 2.149412, 2.1525, 2.155588, 2.158677, 2.161765, 2.165882, 2.17, 2.174118, 2.176588, 2.179059, 2.18153, 2.184, 2.186471, 2.189559, 2.192647, 2.195735, 2.198824, 2.202941, 2.207059, 2.211177, 2.214265, 2.217353, 2.220441, 2.22353, 2.226618, 2.229706, 2.232794, 2.235883, 2.238971, 2.242059, 2.245147, 2.248235, 2.251324, 2.254412, 2.2575, 2.260588, 2.264706, 2.268824, 2.272941, 2.277059, 2.281177, 2.285294, 2.287353, 2.289412, 2.291471, 2.29353, 2.295588, 2.297647, 2.300735, 2.303824, 2.306912, 2.31, 2.313088, 2.316177, 2.319265, 2.322353, 2.325441, 2.32853, 2.331618, 2.334706, 2.337794, 2.340883, 2.343971, 2.347059, 2.350147, 2.353235, 2.356324, 2.359412, 2.365588, 2.371765, 2.375882, 2.38, 2.384118, 2.386588, 2.389059, 2.39153, 2.394, 2.396471, 2.399559, 2.402647, 2.405735, 2.408823, 2.411912, 2.415, 2.418088, 2.421176, 2.425294, 2.429412, 2.433529, 2.436, 2.438471, 2.440941, 2.443412, 2.445882, 2.448971, 2.452059, 2.455147, 2.458235, 2.461323, 2.464412, 2.4675, 2.470588, 2.473676, 2.476765, 2.479853, 2.482941, 2.487059, 2.491177, 2.495294, 2.497765, 2.500235, 2.502706, 2.505177, 2.507647, 2.509706, 2.511765, 2.513824, 2.515882, 2.517941, 2.52, 2.523088, 2.526176, 2.529265, 2.532353, 2.535441, 2.538529, 2.541618, 2.544706, 2.547794, 2.550882, 2.553971, 2.557059, 2.560147, 2.563235, 2.566324, 2.569412, 2.5725, 2.575588, 2.578676, 2.581765, 2.584853, 2.587941, 2.591029, 2.594118, 2.596588, 2.599059, 2.60153, 2.604, 2.606471, 2.609559, 2.612647, 2.615735, 2.618824, 2.621294, 2.623765, 2.626235, 2.628706, 2.631176, 2.634265, 2.637353, 2.640441, 2.643529, 2.646, 2.648471, 2.650941, 2.653412, 2.655882, 2.658353, 2.660824, 2.663294, 2.665765, 2.668235, 2.672353, 2.676471, 2.680588, 2.682647, 2.684706, 2.686765, 2.688824, 2.690882, 2.692941, 2.697059, 2.701177, 2.705294, 2.707353, 2.709412, 2.711471, 2.71353, 2.715588, 2.717647, 2.720735, 2.723824, 2.726912, 2.73, 2.732059, 2.734118, 2.736176, 2.738235, 2.740294, 2.742353, 2.744824, 2.747294, 2.749765, 2.752235, 2.754706, 2.758824, 2.762941, 2.767059, 2.769118, 2.771177, 2.773235, 2.775294, 2.777353, 2.779412, 2.781882, 2.784353, 2.786824, 2.789294, 2.791765, 2.794235, 2.796706, 2.799177, 2.801647, 2.804118, 2.806588, 2.809059, 2.81153, 2.814, 2.816471, 2.81853, 2.820588, 2.822647, 2.824706, 2.826765, 2.828824, 2.831294, 2.833765, 2.836236, 2.838706, 2.841177, 2.842721, 2.844265, 2.845809, 2.847353, 2.848897, 2.850441, 2.851985, 2.853529, 2.856, 2.858471, 2.860941, 2.863412, 2.865882, 2.868353, 2.870824, 2.873294, 2.875765, 2.878235, 2.88, 2.881765, 2.883529, 2.885294, 2.887059, 2.888824, 2.890588, 2.893059, 2.89553, 2.898, 2.900471, 2.902941, 2.904706, 2.906471, 2.908235, 2.91, 2.911765, 2.91353, 2.915294, 2.917765, 2.920235, 2.922706, 2.925177, 2.927647, 2.929706, 2.931765, 2.933824, 2.935883, 2.937941, 2.94, 2.941765, 2.94353, 2.945294, 2.947059, 2.948823, 2.950588, 2.952353, 2.954823, 2.957294, 2.959765, 2.962235, 2.964706, 2.966471, 2.968235, 2.97, 2.971765, 2.973529, 2.975294, 2.977059, 2.979118, 2.981177, 2.983235, 2.985294, 2.987353, 2.989412, 2.990956, 2.9925, 2.994044, 2.995588, 2.997132, 2.998676, 3.000221, 3.001765, 3.004235, 3.006706, 3.009177, 3.011647, 3.014118, 3.015882, 3.017647, 3.019412, 3.021177, 3.022941, 3.024706, 3.026471, 3.028235, 3.03, 3.031765, 3.03353, 3.035294, 3.037059, 3.038824, 3.040368, 3.041912, 3.043456, 3.045, 3.046544, 3.048088, 3.049633, 3.051177, 3.053236, 3.055294, 3.057353, 3.059412, 3.061471, 3.063529, 3.065294, 3.067059, 3.068824, 3.070588, 3.072353, 3.074118, 3.075882, 3.077941, 3.08, 3.082059, 3.084118, 3.086176, 3.088235, 3.091324, 3.094412, 3.0975, 3.125294]

NOM_RES = 10000
SER_RES = 9820
TEMP_NOM = 25
NUM_SAMPLES = 25
THERM_B_COEFF = 3950
ADC_MAX = 1023
ADC_Vmax = 3.15

def init_temp_sensor(TENP_SENS_ADC_PIN_NO = 32):
    adc = ADC(Pin(TENP_SENS_ADC_PIN_NO))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    return adc

def read_temp(temp_sens):
    raw_read = []
    # Collect NUM_SAMPLES
    for i in range(1, NUM_SAMPLES+1):
        raw_read.append(temp_sens.read())

    # Average of the NUM_SAMPLES and look it up in the table
    raw_average = sum(raw_read)/NUM_SAMPLES
    print('raw_avg = ' + str(raw_average))
    print('V_measured = ' + str(adc_V_lookup[round(raw_average)]))

    # Convert to resistance
    raw_average = ADC_MAX * adc_V_lookup[round(raw_average)]/ADC_Vmax
    resistance = (SER_RES * raw_average) / (ADC_MAX - raw_average)
    print('Thermistor resistance: {} ohms'.format(resistance))

    # Convert to temperature
    steinhart  = log(resistance / NOM_RES) / THERM_B_COEFF
    steinhart += 1.0 / (TEMP_NOM + 273.15)
    steinhart  = (1.0 / steinhart) - 273.15
    return steinhart