/*
 * erika.c
 *
 *  Created on: Jun 8, 2018
 *      Author: skauffma
 *
 *    nfer - a system for inferring abstractions of event streams
 *   Copyright (C) 2017  Sean Kauffman
 *
 *   This file is part of nfer.
 *   nfer is free software: you can redistribute it and/or modify
 *   it under the terms of the GNU General Public License as published by
 *   the Free Software Foundation, either version 3 of the License, or
 *   (at your option) any later version.
 *
 *   This program is distributed in the hope that it will be useful,
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *   GNU General Public License for more details.
 *
 *   You should have received a copy of the GNU General Public License
 *   along with this program.  If not, see <https://www.gnu.org/licenses/>.
 */


/*********
 * This file isn't meant to be compiled with the main application.
 * It is here to be included with "compiled" monitors where the target OS is Erika
 *********/

#if TARGET==erika
// include definitions for the log functions
static int log_level = DEFAULT_LOG_LEVEL;
void set_log_level(int level) {
    log_level = level;
}

void filter_log_msg(int level, const char *message, ...) {
    va_list args;
    va_start(args, message);

    if (level <= log_level) {
        printk(message, args);
    }

    va_end(args);
}

void log_msg(const char *message, ...) {
    va_list args;
    va_start(args, message);

    printk(message, args);

    va_end(args);
}

bool should_log(int level) {
    return level <= log_level;
}

void write_msg(int log_to, const char *message, ...) {
    va_list args;
    va_start(args, message);

    printk(message, args);

    va_end(args);
}

SemType V;
DeclareTask(Task1);
struct ivshmem_dev_data {
    u16 bdf;
    u32 *registers;
    void *shmem;
    u64 shmemsz;
    u64 bar2sz;
};
typedef struct data_format {
    double timestamp;
    float data;
    float frequency;
    char channel_name[48];
} data_format_t;
struct ivshmem_dev_data *d = NULL;
static struct ivshmem_dev_data devs[4];

// for Erika, this should be a task
TASK(Task1) {
    volatile data_format_t * data = (data_format_t *) d->shmem;
    map_value value;
    map_key data_key, frequency_key;
    bool read_success;
    interval *interval_to_add;

    init_nfer();

    interval_to_add = allocate_interval(&input_pool);

    data_key = find_word(&global_key_dict, "data");
    frequency_key = find_word(&global_key_dict, "frequency");
    while (true) {
        filter_log_msg(LOG_LEVEL_DEBUG, "nfer Waiting for the semaphore\n");
        WaitSem(&V);
        filter_log_msg(LOG_LEVEL_DEBUG, "nfer | Timestamp=%d | Data=%d | d->shmem = %p | channel = %s\n",
                (int) data->timestamp, (int) data->data, (void *) d->shmem, data->channel_name);
        interval_to_add->name = find_word(&global_name_dict, (const char *)data->channel_name);
        interval_to_add->start = (timestamp)data->timestamp;
        interval_to_add->end = interval_to_add->start;
        if (data_key != MAP_MISSING_KEY) {
            value.type = real_type;
            value.real_value = data->data;
            map_set(&interval_to_add->map, data_key, &value);
        }
        if (frequency_key != MAP_MISSING_KEY) {
            value.type = real_type;
            value.real_value = data->frequency;
            map_set(&interval_to_add->map, frequency_key, &value);
        }
        read_success = true;

        if (read_success) {
            wakeup();
            interval_to_add = allocate_interval(&input_pool);
        }
    }

    return;
}

/* ###*B*###
 * Erika Enterprise, version 3
 *
 * Copyright (C) 2017 Evidence s.r.l.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or (at
 * your option) any later version.
 *
 * This program is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * General Public License, version 2, for more details.
 *
 * You should have received a copy of the GNU General Public License,
 * version 2, along with this program; if not, see
 * <https://www.gnu.org/licenses/old-licenses/gpl-2.0.html >.
 *
 * This program is distributed to you subject to the following
 * clarifications and special exceptions to the GNU General Public
 * License, version 2.
 *
 * THIRD PARTIES' MATERIALS
 *
 * Certain materials included in this library are provided by third
 * parties under licenses other than the GNU General Public License. You
 * may only use, copy, link to, modify and redistribute this library
 * following the terms of license indicated below for third parties'
 * materials.
 *
 * In case you make modified versions of this library which still include
 * said third parties' materials, you are obligated to grant this special
 * exception.
 *
 * The complete list of Third party materials allowed with ERIKA
 * Enterprise version 3, together with the terms and conditions of each
 * license, is present in the file THIRDPARTY.TXT in the root of the
 * project.
 * ###*E*### */

#define VENDORID    0x1af4
#define DEVICEID    0x1110
#define IVSHMEM_CFG_SHMEM_PTR   0x40
#define IVSHMEM_CFG_SHMEM_SZ    0x48
#define JAILHOUSE_SHMEM_PROTO_UNDEFINED 0x0000
#define IVSHMEM_IRQ 149
#define IVSHMEM_PCI_REG_ADDR 0xfc100000
#define SHARED_MEM_SIZE     0x100000

volatile char *shmem;
static int irq_counter;

static u64 pci_cfg_read64(u16 bdf, unsigned int addr)
{
    u64 bar;

    bar = ((u64)arm_pci_read_config(bdf, addr + 4, 4) << 32) |
          arm_pci_read_config(bdf, addr, 4);
    return bar;
}

static void pci_cfg_write64(u16 bdf, unsigned int addr, u64 val)
{
    arm_pci_write_config(bdf, addr + 4, (u32)(val >> 32), 4);
    arm_pci_write_config(bdf, addr, (u32)val, 4);
}

static u64 get_bar_sz(u16 bdf, u8 barn)
{
    u64 bar, tmp;
    u64 barsz;

    bar = pci_cfg_read64(bdf, PCI_CFG_BAR + (8 * barn));
    pci_cfg_write64(bdf, PCI_CFG_BAR + (8 * barn), 0xffffffffffffffffULL);
    tmp = pci_cfg_read64(bdf, PCI_CFG_BAR + (8 * barn));
    barsz = ~(tmp & ~(0xf)) + 1;
    pci_cfg_write64(bdf, PCI_CFG_BAR + (8 * barn), bar);

    return barsz;
}

static int map_shmem_and_bars(struct ivshmem_dev_data *d)
{
    d->shmemsz = pci_cfg_read64(d->bdf, IVSHMEM_CFG_SHMEM_SZ);
    d->shmem = (void *)((u64)(0xffffffffffffffff & pci_cfg_read64(d->bdf, IVSHMEM_CFG_SHMEM_PTR)));

    printk("nfer: shmem is at %p, shmemsz is %p\n", d->shmem, d->shmemsz);
    d->registers = (u32 *) IVSHMEM_PCI_REG_ADDR; //added by Giovani
    pci_cfg_write64(d->bdf, PCI_CFG_BAR, (u64)d->registers);
    printk("nfer: bar0 is at %p\n", d->registers);
    d->bar2sz = get_bar_sz(d->bdf, 2);

    arm_pci_write_config(d->bdf, PCI_CFG_COMMAND,
             (PCI_CMD_MEM | PCI_CMD_MASTER), 2);
    return 0;
}

static u32 get_ivpos(struct ivshmem_dev_data *d)
{
    return mmio_read32(d->registers + 2);
}

static void send_irq(struct ivshmem_dev_data *d)
{
    printk("nfer: sending IRQ - addr = %p\n", (d->registers + 3));
    mmio_write32(d->registers + 3, 1);
}

static void enable_irq(struct ivshmem_dev_data *d)
{
    printk("nfer: Enabling IVSHMEM_IRQs registers = %p\n", d->registers);
    mmio_write32(d->registers, 0xffffffff);
}


void handle_IRQ(void);
void handle_IRQ(void)
{
    printk("nfer: handle_irq() - interrupt #%d, sem %d\n", ++irq_counter, V.count);
    PostSem(&V);
}


void idle_hook(void);
void idle_hook(void) {
    while(1) {
        asm volatile("wfi" : : : "memory");
    }
}

TaskType task1_id;

int main(void) {
    unsigned int i = 0;
    int bdf = 0;
    unsigned int class_rev;
    int ndevices = 0;
    TaskType isr_ivshmem;

    /* Initialization of the semaphore */
    InitSem(&V, 0);

    StatusType s = E_OK;

    s |= CreateTask( &isr_ivshmem, OSEE_TASK_TYPE_ISR2, handle_IRQ, 1U, 1U, 1U, OSEE_SYSTEM_STACK );
    /* Tie ISR2 With IRQ */
    SetISR2Source(isr_ivshmem, IVSHMEM_IRQ);

    s |= CreateTask( &task1_id, OSEE_TASK_TYPE_EXTENDED, TASK_FUNC(Task1), 1U, 1U, 1U, 1024 );

    printk("nfer: All TASKs created with result (0 is OK):%d\n", s);

    if(-1 != (bdf = pci_find_device(VENDORID, DEVICEID, bdf))) {
        printk("nfer: Found %04x:%04x at %02x:%02x.%x\n",
               arm_pci_read_config(bdf, PCI_CFG_VENDOR_ID, 2),
               arm_pci_read_config(bdf, PCI_CFG_DEVICE_ID, 2),
               bdf >> 8, (bdf >> 3) & 0x1f, bdf & 0x3);
        class_rev = arm_pci_read_config(bdf, 0x8, 4);
        if (class_rev != (PCI_DEV_CLASS_OTHER << 24 |
                  JAILHOUSE_SHMEM_PROTO_UNDEFINED << 8)) {
            printk("nfer: class/revision %08x, not supported skipping device\n", class_rev);

            return 0;
        }
        ndevices++;
        d = devs + ndevices - 1;
        d->bdf = bdf;
        if (map_shmem_and_bars(d)) {
            printk("nfer: Failure mapping shmem and bars.\n");
            return 0;
        }

        printk("nfer: mapped shmem and bars, got position %p - bdf = %d\n", get_ivpos(d), bdf);

        printk("nfer: Enabled IRQ:0x%x\n", IVSHMEM_IRQ +  ndevices -1);

        enable_irq(d);

        //bdf++;

    }

    if (!ndevices) {
        printk("nfer: No PCI devices found .. nothing to do.\n");
        return 0;
    }

    printk("nfer: Done setting up...\n");

    for (i = 0; i < ndevices; i++) {
        d = devs + i;
        shmem = d->shmem;
        shmem[19]++;
        printk("nfer: sending interrupt.\n");
        send_irq(d);
    }

    printk("nfer | Before | Call StartOS\n");
    printk("nfer | Before | Interrupt Enabled? (0=No)<%d>, PMR:<%x>\n",
    osEE_hal_is_enabledIRQ(), osEE_gicc_read_pmr());
    StartOS(OSDEFAULTAPPMODE);

    ActivateTask(task1_id);

    printk("nfer | Returned from application main\n");
    return 0;
}
#endif

